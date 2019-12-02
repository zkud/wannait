# Журнал Реализации
Данный документ отражает примененные паттерны проектирования и шаблоны рефакторинга во время реализации проекта.
## Паттерны проектирования
[Ссылка на диаграмму классов](https://github.com/L1ttl3S1st3r/wannait/blob/master/Documents/Design/Class/Readme.md)  
* Стратегия (Классы RecommendationsSearchAlgorithm, FactorizationAlgorithm, TopRatingsAlgorithm), потому что есть несколько алгоритмов рекомендации, нужно обеспечить расширяемость (возможность быстрого добавления новых алгоритмов) [(Ссылка на код)](https://github.com/L1ttl3S1st3r/wannait/blob/master/Source/wannait/backend_server/models.py)    
* Фабрика (Класс RecommendationsSearchAlgorithmFactory), потому что нужно порождать объекты, связанные с предыдущим паттерном, а обычный конструктор не подойдёт. [(Ссылка на код)](https://github.com/L1ttl3S1st3r/wannait/blob/master/Source/wannait/backend_server/models.py)    
* Одиночка (Класс FactorizationModel), потому что нужно гарантировать единственность экземпляра для всех пользователей, предоставить глобальную точку доступаю. [(Ccылка на код)](https://github.com/L1ttl3S1st3r/wannait/blob/master/Source/wannait/backend_server/ml.py)  
* DAO (Классы в DAO Layer), так как нужно обеспечить удобный интерфейс с Базой Данных. [(Ссылка на код)](https://github.com/L1ttl3S1st3r/wannait/blob/master/Source/wannait/backend_server/models.py)    
## Архитектурные шаблоны
* разделение на Frontend и Backend серверы, чтобы обеспечить выполнение требования к масштабируемости.  
* MVC, чтобы разделить GUI и бизнес-логику.  
* Большая часть View's бэкенд-сервера ведут себя согласно REST [(одно из объяснений REST)](https://medium.com/@andr.ivas12/rest-%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%8B%D0%BC-%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%BC-90a0bca0bc78), кроме Recommendations View (потому что там присутствует реальная необходимость хранить состояние). 
## Шаблоны рефакторинга  
* Выделение класса (класс cо слишком большим количеством обязанностей ProductView заменён на ProductViewSet, CommentViewSet, LikeView, DetailedProductView, VisitView).
* Переход к применению вышеописанных паттернов проектирования (до этого фабрика и одиночка не применялись).  
* Отход от паттерна проектирования Состояние (Раньше было много классов, отвечаюших за состояние интерфейса, теперь только ProductInfoView).
