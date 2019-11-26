print('RETRAIN RUNS!')
import torch
import numpy as np
import math

from .models import BackendLike
from .models import BackendVisit
from backend_server.factorization_result import FactorizationResult


n_factors = 20 # количество строк (столбцов) в матрицах факторов


print('Start Selecting')
# form ratings matrix
likes_stats_user = BackendLike.objects.all().values('owner').distinct()
likes_stats_product = BackendLike.objects.all().values('product').distinct()
visits_stats_user = BackendVisit.objects.all().values('owner').distinct()
visits_stats_product = BackendVisit.objects.all().values('product').distinct()
n_users = likes_stats_user.union(visits_stats_user).count()
n_products = likes_stats_product.union(visits_stats_product).count()
ratings = np.full((n_users, n_products), np.nan, dtype=np.float32)
recommendations = np.zeros((n_users, n_products), dtype=np.int64)

# form rating matrix and maps
result = FactorizationResult({}, recommendations)
products_dict = {}
inverse_product_map = np.zeros((n_products,), dtype=np.int64)
row_counter = 0
col_counter = 0
for visit in BackendVisit.objects.all():
    row, col = 0, 0
    if visit.owner.id in result.user_dict.keys():
        row = result.user_dict[visit.owner.id]
    else:
        result.user_dict[visit.owner.id] = row_counter
        row_counter += 1

    if visit.product.id in products_dict.keys():
        col = products_dict[visit.product.id]
    else:
        products_dict[visit.product.id] = col_counter
        inverse_product_map[col_counter] = visit.product.id
        col_counter += 1

    ratings[row, col] = 0.0

for like in BackendLike.objects.all():
    row, col = 0, 0
    if like.owner.id in result.user_dict.keys():
        row = result.user_dict[like.owner.id]
    else:
        result.user_dict[like.owner.id] = row_counter
        row_counter += 1

    print(products_dict)
    print(like.product.id)
    if like.product.id in products_dict.keys():
        col = products_dict[like.product.id]
    else:
        products_dict[like.product.id] = col_counter
        inverse_product_map[col_counter] = like.product.id
        col_counter += 1

    ratings[row, col] = 1.0


lambda_parameter = math.sqrt(1 / n_factors)


indexes = np.where(~np.isnan(ratings))

# параметры обучения (не все, смотри ниже в train)
print(len(indexes[0]))
test_split = len(indexes[0]) // 20
epochs = 50 #количество эпох обучения
epoch_part = len(indexes[0]) // 3 # количество кортежей (пользователь, продукт, оценка), используемое за эпоху
print(test_split)
print(epoch_part)

order = np.arange(len(indexes[0]))
np.random.shuffle(order)
indexes = (indexes[0][order], indexes[1][order])
test_indexes = (indexes[0][:test_split], indexes[1][:test_split])
indexes = (indexes[0][test_split:], indexes[1][test_split:])

print(test_indexes)
print(indexes)

print("ratings matrix {}".format(ratings))

print('End Selecting, start training')
class MatrixFactorization(torch.nn.Module):
    def __init__(self, n_users, n_products, lambda_parameter, n_factors=20):
        super().__init__()
        self.user_factors = torch.nn.Parameter(torch.full((n_users, n_factors), lambda_parameter, dtype=torch.float32),
                                               requires_grad=True)
        self.product_factors = torch.nn.Parameter(
            torch.full((n_factors, n_products), lambda_parameter, dtype=torch.float32),
            requires_grad=True)

    def forward(self, user, product):
        return torch.mm(self.user_factors[user, :],
                        self.product_factors[:, product])

    def predict(self, user, product):
        return self.forward(user, product)

    def predict_all(self):
        return torch.mm(self.user_factors, self.product_factors)


model = MatrixFactorization(n_users, n_products, lambda_parameter, n_factors=n_factors)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)
print("using device {}".format(device))
print("model parameters:")
for parameter in model.parameters():
    print(parameter)
    print(parameter.shape)


loss_func = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(),
                             lr=1e-3)


def train():
    train_loss_history = []
    val_loss_history = []
    phases = ['train', 'val']
    # mech.....
    global epochs
    global indexes
    global optimizer
    global model
    global epoch_part
    global ratings
    global device
    global loss_func

    for epoch in range(epochs):
        print('\n\nEpoch {} / {}'.format(epoch, epochs))
        # shuffle data
        order = np.arange(len(indexes[0]))
        np.random.shuffle(order)
        train_order = order[:epoch_part]
        val_order = order[epoch_part:2 * epoch_part]

        for phase in phases:
            if phase == 'train':
                optimizer.zero_grad()
                current_order = train_order
                current_indexes = (indexes[0][train_order], indexes[1][train_order])
                history = train_loss_history
            else:
                current_order = val_order
                current_indexes = (indexes[0][val_order], indexes[1][val_order])
                history = val_loss_history

            rating = ratings[current_indexes[0], :][:, current_indexes[1]]
            prediction = model.predict(current_indexes[0], current_indexes[1]).to(device)
            # form mask array
            mask = torch.zeros(rating.shape)
            normal_poses = np.where(~np.isnan(rating))
            for pose in zip(normal_poses[0], normal_poses[1]):
                mask[pose[0], pose[1]] = 1
            rating = np.nan_to_num(rating)
            rating = torch.tensor(rating, dtype=torch.float32, device=device)
            mask = mask.to(device)

            rating *= mask
            prediction *= mask

            loss = loss_func(prediction, rating)
            running_loss = loss.data.cpu()
            print('{} loss {}'.format(phase, running_loss))
            history.append(running_loss)
            if phase == 'train':
                loss.backward()

                optimizer.step()

    return train_loss_history, val_loss_history


history = train()


if len(test_indexes[0]) > 0:
    rating = torch.tensor(ratings[test_indexes[0], :][:, test_indexes[1]], dtype=torch.float32)
    prediction = model.predict(test_indexes[0], test_indexes[1]).to(device)


    # form mask array
    mask = torch.ones(rating.shape)
    nan_poses = np.where(np.isnan(rating))
    for pose in zip(nan_poses[0], nan_poses[1]):
        mask[pose[0], pose[1]] = 0
        rating[pose[0], pose[1]] = 0
    rating = rating.to(device)
    mask = mask.to(device)


    rating *= mask
    prediction *= mask


    loss = loss_func(prediction, rating)
    test_loss = loss.data.cpu()
    print('Sucessfully finished training. Test loss {}'.format(test_loss))
else:
    print('Sucessfully finished training!')


predictions = model.predict_all().cpu().detach().numpy()
print(predictions)
print(result.user_dict)

# for every user
for user_id, row in result.user_dict.items():
    # form -sorted list[(index_of_product, product_prediction)]
    print(predictions.shape)
    user_prediction = predictions[row, :]
    predictions_pairs = [
        (index, pred)
        for index, pred in zip(
            inverse_product_map,
            user_prediction
        )
    ]
    predictions_pairs.sort(reverse=True, key=lambda pair: pair[1])

    # dump list content into recommendations
    for index, pair in enumerate(predictions_pairs):
        result.recommendations[row, index] = pair[0]

print(result.recommendations)
result.save()

