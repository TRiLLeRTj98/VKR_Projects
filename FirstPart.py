#!/usr/bin/env python
# coding: utf-8

# # Многоклассовая классификация изображений

# ### Импорт библиотек
# 
# #### В этом разделе мы импортируем библиотеки, которые будем использовать. В случае, если библиотека отсутсвует, скачаем её через pip install.

# In[8]:


import pandas as pd
import numpy as np
import os
from tensorflow.keras.layers import Dense, Input, InputLayer, Flatten
from tensorflow.keras.models import Sequential, Model
import tensorflow as tf
import cv2
from tensorflow import keras
import matplotlib.image as mpimg
import warnings
from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.models import Sequential, Model
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier

warnings.filterwarnings("ignore")


# #### Установка размера изображения и исходной папки для загрузки набора данных

# In[9]:


IMG_WIDTH=200
IMG_HEIGHT=200
img_folder=r'/content/training/Coat'


# #### Печать случайных 10  изображений из одной из папок

# In[10]:


import random
plt.figure(figsize=(15,15))
test_folder=r'/content/training/Coat'
for j in range(5):
    file = random.choice(os.listdir(img_folder))
    image_path= os.path.join(img_folder, file)
    img=mpimg.imread(image_path)
    ax=plt.subplot(1,5,j+1)
    ax.title.set_text(file)
    plt.imshow(img)


# In[11]:


img_folder=r'/content/training'


# #### В этой части загрузим и создалим набор изображений и набор тестовых данных из пользовательских  в качестве входных данных для моделей глубокого обучения. Загрузка будет происходить с помощью Open CV2

# #### Создание данных изображения и меток из изображений в папке
# #### В функции ниже
# #### Исходная папка — это входной параметр, содержащий изображения для разных классов.
# #### Прочитаем файл изображения из папки и преобразуйте его в правильный цветовой формат.
# #### Изменим размер изображения на основе входного размера, необходимого для модели.
# #### Преобразуем изображение в массив Numpy с float32 в качестве типа данных.
# #### Нормируем массив изображений, чтобы его значения были уменьшены от 0 до 1 от 0 до 255 для аналогичного распределения данных, что способствует более быстрой сходимости.

# In[12]:


def create_dataset(img_folder):
   
    img_data_array=[]
    class_name=[]
   
    for dir1 in os.listdir(img_folder):
        for file in os.listdir(os.path.join(img_folder, dir1)):
       
            image_path= os.path.join(img_folder, dir1,  file)
            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
            image=np.array(image)
            image = image.astype('float32')
            image /= 255 
            img_data_array.append(image)
            class_name.append(dir1)
    return img_data_array, class_name


# In[13]:


img_data, class_name =create_dataset(r'./training')


# #### Извлечем массив изображений и метки класса
# 

# In[14]:


target_dict={k: v for v, k in enumerate(np.unique(class_name))}
target_dict


# #### Преобразование текстовых меток в числовые коды

# In[15]:


target_val=  [target_dict[class_name[i]] for i in range(len(class_name))]


# #### Создание простой модели глубокого обучения и ее компиляция

# In[16]:


import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# In[17]:


model=tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(input_shape=(IMG_HEIGHT,IMG_WIDTH, 3)),
            tf.keras.layers.Conv2D(filters=32, kernel_size=3, strides=(2, 2), activation='relu'),
            tf.keras.layers.Conv2D(filters=64, kernel_size=3, strides=(2, 2), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(9)
        ])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# In[18]:


model.summary()


# #### Фильтры
# 
# ![image.png](attachment:image.png)

# Первый обязательный параметр Conv2D — это количество фильтров, которые будет изучать сверточный слой.
# 
# Слои в ранней сетевой архитектуре (т. е. ближе к фактическому входному изображению) изучают меньше сверточных фильтров, в то время как более глубокие слои в сети (т. е. ближе к выходным прогнозам) изучают больше фильтров.
# 
# Промежуточные слои Conv2D изучают больше фильтров, чем ранние слои Conv2D, но меньше фильтров, чем слои, расположенные ближе к выходным данным.

# #### Размер_ядра
# 
# ![image.png](attachment:image.png)

# Второй обязательный параметр, который необходимо предоставить классу Keras Conv2D, — это kernel_size, состоящий из двух кортежей, указывающий ширину и высоту окна 2D-свертки.
# 
# Размер ядра также должен быть нечетным целым числом.
# 
# Типичные значения для kernel_size включают: (1, 1) , (3, 3) , (5, 5) , (7, 7) . Редко можно увидеть размеры ядра больше 7×7.
# 
# Итак, когда вы используете каждый из них?
# 
# Если ваши входные изображения больше 128 × 128, вы можете использовать размер ядра> 3, чтобы помочь (1) изучить более крупные пространственные фильтры и (2) помочь уменьшить размер объема.
# 
# Другие сети, такие как VGGNet, используют исключительно фильтры (3, 3) во всей сети.
# 
# Более продвинутые архитектуры, такие как Inception, ResNet и SqueezeNet, проектируют целые микроархитектуры, представляющие собой «модули» внутри сети, которые изучают локальные особенности в разных масштабах (например, 1×1, 3×3 и 5×5), а затем объединяют выходы.

# ### СДВИГИ

# Параметр strides представляет собой набор из двух целых чисел, указывающих «шаг» свертки по осям x и y входного объема.
# 
# Значение шага по умолчанию равно (1, 1) , что означает, что:
# 
# Данный сверточный фильтр применяется к текущему местоположению входного объема.
# Фильтр делает шаг на 1 пиксель вправо и снова фильтр применяется к входному объему.
# Этот процесс выполняется до тех пор, пока мы не достигнем крайней правой границы объема, в котором мы перемещаем наш фильтр на один пиксель вниз, а затем снова начинаем с крайнего левого.
# Обычно вы оставляете параметр strides со значением по умолчанию (1, 1); однако иногда можно увеличить его до (2, 2), чтобы уменьшить размер выходного тома (поскольку размер шага фильтра больше).

# ### Функция активации
# 
# ![image.png](attachment:image.png)

# Параметр активации для класса Conv2D — это просто параметр удобства, позволяющий указать строку, указывающую имя функции активации, которую мы хотим применить после выполнения свертки.
# 
# В нашем примере мы выполняем свертку, а затем применяем функцию активации ReLU:

# ### Наконец-то мы подогнали наш набор данных для обучения модели. Мы можем использовать массив Numpy в качестве входных данных

# In[19]:


history = model.fit(x=np.array(img_data, np.float32), y=np.array(list(map(int,target_val)), np.float32),validation_split=0.2, epochs=50)


# In[20]:


print(history.history.keys())


# In[ ]:


# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# Как мы видим, при небольшом количестве данных нейронные сети дают очень плохой результат  

# #### Давайте попытаемся использовать нащи данные для обучения на более простых моделях, чем нейронные сети, к примеру на ансамблевом обучении. 

# In[22]:


nsamples, nx, ny,_ = np.array(img_data).shape
img_data = np.array(img_data).reshape((nsamples,nx*ny*3))
X_train, X_test, y_train, y_test = train_test_split(img_data, target_val, test_size=0.2, random_state=42)


# #### Ансамблевое обучение в целом представляет собой модель, которая делает прогнозы на основе ряда различных моделей. Комбинируя отдельные модели, модель ансамбля становится более гибкой🤸‍♀️ (меньше предвзятости) и менее чувствительной к данным🧘‍♀️ (меньше дисперсии).

# Двумя наиболее популярными ансамблевыми методами являются бэггинг и бустинг.
# 
# Бэггинг: параллельное обучение нескольких отдельных моделей. Каждая модель обучается на случайном подмножестве данных
# 
# Бустинг: последовательное обучение группы отдельных моделей. Каждая отдельная модель учится на ошибках, допущенных предыдущей моделью.

# ### 1 Случайный лес
# Случайный лес — это модель ансамбля, использующая бэггинг в качестве метода ансамбля и дерево решений в качестве отдельной модели.

# In[23]:


# Шаг 1: Подгонка модели дерева решений
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
accuracy_score(y_test, y_pred)


# In[24]:


# Шаг 2: Сопоставьте модель случайного леса
clf = RandomForestClassifier(n_estimators=100, max_features="auto",random_state=0)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
accuracy_score(y_test, y_pred)


# ### AdaBoost (адаптивное повышение)
# AdaBoost — это повышающая ансамблевая модель, которая особенно хорошо работает с деревом решений. Ключом к модели повышения является обучение на предыдущих ошибках, т.е. точки данных неправильной классификации.
# AdaBoost учится на ошибках, увеличивая вес ошибочно классифицированных точек данных.

# In[35]:


# Шаг 3: модель AdaBoost
clf = AdaBoostClassifier(n_estimators=100)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
accuracy_score(y_test, y_pred)


# In[ ]:


from sklearn.model_selection import GridSearchCV
params = {
     'n_estimators': np.arange(10,300,100),
     'learning_rate': [0.01, 0.05, 0.1, 1],
 }
grid_cv = GridSearchCV(AdaBoostClassifier(), param_grid= params, cv=5, n_jobs=-1)
grid_cv.fit(X_train, y_train)
grid_cv.best_params_


# In[ ]:



accuracy_score(y_test, grid_cv.predict(grid_cv))


# ### Градиентный бустинг
# Градиентный бустинг — еще одна модель повышения. Ключом к повышению эффективности модели является обучение на предыдущих ошибках.
# Gradient Boosting учится на ошибке — остаточной ошибке напрямую, а не обновляет веса точек данных.

# In[ ]:


# Шаг 4: модель повышения градиента
clf = GradientBoostingClassifier(n_estimators=100)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
accuracy_score(y_test, y_pred)


# In[ ]:


from sklearn.ensemble import GradientBoostingClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import make_scorer
#создание параметра оценки:

scoring = {'accuracy': make_scorer(accuracy_score),
           'precision': make_scorer(precision_score),'recall':make_scorer(recall_score)}

# Пример параметра
parameters = {
    "loss":["deviance"],
    "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
    "min_samples_split": np.linspace(0.1, 0.5, 12),
    "min_samples_leaf": np.linspace(0.1, 0.5, 12),
    "max_depth":[3,5,8],
    "max_features":["log2","sqrt"],
    "criterion": ["friedman_mse",  "mae"],
    "subsample":[0.5, 0.618, 0.8, 0.85, 0.9, 0.95, 1.0],
    "n_estimators":[10]
    }
# передача функции подсчета очков в GridSearchCV
clf = GridSearchCV(GradientBoostingClassifier(), parameters,scoring=scoring,refit=False,cv=2, n_jobs=-1)

clf.fit(X_train, y_train)
# преобразование clf.cv_results в фрейм данных
df=pd.DataFrame.from_dict(clf.cv_results_)
#здесь Возможные входные данные для перекрестной проверки: cv=2, есть два разделения split0 и split1
df[['split0_test_accuracy','split1_test_accuracy','split0_test_precision','split1_test_precision','split0_test_recall','split1_test_recall']]


# In[ ]:


#найти лучший параметр на основе precision_score
# взяв среднее значение по показателю "точность_показателя"
df['accuracy_score']=(df['split0_test_accuracy']+df['split1_test_accuracy'])/2

df.loc[df['accuracy_score'].idxmax()]['params']


# В целом, ансамблевое обучение очень мощное и может использоваться не только для решения задачи классификации, но и для регрессии. Но в задачах классификации изображений они все же не пользуются большой популярностью, так как при больших массивах данных становятся просто напросто очень долгими и не такими эффективными, как нейронные сети.
