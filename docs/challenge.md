El modelo escogido fue el de XGBoost con Feature Importance y con Balance. Esto se debe a que si bien segun el reporte de
clasificación separecen mucho los modelos de XGBoost con el de LogisticRegression, se ve que para XGBoost existe un 0.01 más de puntaje de f1-score y un 0.01 de macro avg para el recall. Este pequeño aumento de las metricas son lo que determina la decisión final.
