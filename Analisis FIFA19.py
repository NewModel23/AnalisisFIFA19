#!/usr/bin/env python
# coding: utf-8

# # Análisis de FIFA19

# In[1]:


# Importar las librerías a utilizar
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import median
from statistics import mode


# In[2]:


os.getcwd()


# In[3]:


os.listdir()


# In[4]:


df = pd.read_csv('data.csv')


# In[19]:


pd.set_option('display.max_columns', 100)
df.head()


# Realizar limpieza de los datos (eliminar columnas no necesarias, convertir la columna Wage a formato numérico y multiplicar las 'k' por 1000 al igual que las 'M' por 1,000,000

# In[6]:


# Quitar las columnas que no necesitaremos
columnas = ['Unnamed: 0','Photo','Flag','Club Logo','Loaned From']
df.drop(columnas, axis = 1, inplace=True)


# In[18]:


df.head()


# In[8]:


# Convertir los valores de 'Value' y 'Wages' a números, multiplicar la letra 'k' por 1000  y la letra 'M' por 1,000,000
# Así como quitar el carácter de Euros

df['Wage'] = df['Wage'].map(lambda x: x.lstrip('€'))


# In[10]:


df['Wage'].replace(r'[KM]+$', '', regex=True).astype(float)


# In[11]:


df['Wage'].str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(0).replace(['K','M'], [10**3, 10**6]).astype(int)


# In[12]:


df['Wage'] = df['Wage'].replace(r'[KM]+$', '', regex=True).astype(float) * df['Wage'].str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(0).replace(['K','M'], [10**3, 10**6]).astype(int)


# In[14]:


# Quitar Salarios en ceros

df = df[df['Wage']>0]


# In[15]:


# Sustituir los valores NA por 0 para poder agruparlos y promediarlos
df.fillna(0, inplace = True)


# In[16]:


# Agrupación y promedio de características para obtener una calificación y trabajar con ello
def defensa(df):
    return int(round((df[['Marking', 'StandingTackle','SlidingTackle']].mean()).mean()))

def general(df):
    return int(round((df[['HeadingAccuracy', 'Dribbling', 'Curve','BallControl']].mean()).mean()))

def pases(df):
    return int(round((df[['Crossing', 'ShortPassing','LongPassing']].mean()).mean()))
def mobilidad(df):
    return int(round((df[['Acceleration', 'SprintSpeed','Agility','Reactions']].mean()).mean()))
def fuerza(df):
    return int(round((df[['Balance', 'Jumping', 'Stamina','Strength']].mean()).mean()))
def puntuacion(df):
    return int(round((df[['Potential', 'Overall']].mean()).mean()))
def disparos(df):
    return int(round((df[['Finishing', 'Volleys', 'FKAccuracy','ShotPower','LongShots', 'Penalties']].mean()).mean()))


# In[17]:


# Agregar estos cálculos al data frame

df['Defensa'] = df.apply(defensa, axis = 1)
df['General'] = df.apply(general, axis = 1)
df['Pases'] = df.apply(pases, axis = 1)
df['Mobilidad'] = df.apply(mobilidad, axis = 1)
df['Fuerza'] = df.apply(fuerza, axis = 1)
df['Puntuacion'] = df.apply(puntuacion, axis = 1)
df['Disparos'] = df.apply(disparos, axis = 1)


# Realizar análisis básico para concer un poco más acerca de la información
# En mi caso no se mucho de futbol, así que en este video aprenderé un poco.
# Hay mucha información útil, pero eso llevaría mucho tiempo, así que solo haré unos pocos análisis

# In[20]:


# El jugador con la mayor Puntuación
print('Máxima puntuación :' + str(df.loc[df['Puntuacion'].idxmax()][1]))


# In[21]:


# Vamos a tomar las características que a mi forma de ver (No sé mucho de futbol) son indispensables
# Creamos un arreglo
caracteristicas = []
caracteristicas = ['Defensa','General','Pases','Mobilidad','Fuerza','Puntuacion','Disparos']

resultado = []
i=0
while i < len(caracteristicas):
    resultado.append('{1}'.format(caracteristicas[i],df.loc[df[caracteristicas[i]].idxmax()][1]))
    print(caracteristicas[i] + ': {1}'.format(caracteristicas[i],df.loc[df[caracteristicas[i]].idxmax()][1]))
    i += 1

resultado = pd.DataFrame.from_dict(resultado)

resultado.columns=['Jugador']


# In[22]:


mode(resultado['Jugador'])


# In[23]:


# Obtener el jugador que destaca en más características
i=0
while i < len(caracteristicas):
    if df.loc[df[caracteristicas[i]].idxmax()][1] == mode(resultado['Jugador']):
        print('Mejor {0} : {1}'.format(caracteristicas[i],df.loc[df[caracteristicas[i]].idxmax()][1]))
    i += 1


# In[24]:


# Top 5 control de indicadores generales ('HeadingAccuracy', 'Dribbling', 'Curve','BallControl') por nacionalidad
general = df.sort_values('General', ascending = False)[['Nationality','General']].head(5) 
sns.barplot(x = 'Nationality', y = 'General', data = general,estimator=median,capsize=.2)
print(general )


# In[25]:


# Obtener la mobilidad (Agilidad) por edad del jugador
sns.lmplot(data = df, x = 'Age', y = 'Mobilidad',lowess=True, line_kws={'color':'red'},height=8.27, aspect=11.7/8.27)


# In[26]:


# Conteo de jugadores por rangos de edad
sns.set(palette = "colorblind")
x = df['Age']
plt.figure(figsize = (12,8))
ax = sns.distplot(x, bins = 58, kde = False, color = 'g')
ax.set_xlabel(xlabel = "Edad de los jugadores", fontsize = 20)
ax.set_ylabel(ylabel = 'Conteo de jugadores', fontsize = 20)
ax.set_title(label = 'Relación de conteo de jugadores vs Edades', fontsize = 20)
plt.show()


# In[28]:


# Los jugadores de mayor edad
print(df.sort_values('Age', ascending = False)[['Name', 'Age', 'Club', 'Nationality']].head(10) )


# In[29]:


# Obtener el top 5 de las nacionalidades mejor pagadas
df.groupby(['Nationality']).sum()[['Wage']].sort_values('Wage',ascending = False).head(5)

