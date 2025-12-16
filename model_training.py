"""
Model Training Module
Provides basic machine learning model training and evaluation.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    accuracy_score, precision_score, recall_score, f1_score, classification_report
)
from typing import Dict, Tuple, Optional, List
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """Train and evaluate machine learning models."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model_type = None
    
    def prepare_data(self, target_column: str, feature_columns: Optional[List[str]] = None, 
                     test_size: float = 0.2, random_state: int = 42) -> Tuple:
        """
        Prepare data for training by splitting into train and test sets.
        
        Args:
            target_column: Name of the target column
            feature_columns: List of feature columns. If None, use all columns except target.
            test_size: Proportion of data to use for testing
            random_state: Random state for reproducibility
            
        Returns:
            Tuple: (X_train, X_test, y_train, y_test)
        """
        if target_column not in self.df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")
        
        # Select features
        if feature_columns is None:
            feature_columns = [col for col in self.df.columns if col != target_column]
        
        # Only use numerical columns
        numerical_features = self.df[feature_columns].select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numerical_features) == 0:
            raise ValueError("No numerical features found for training")
        
        X = self.df[numerical_features].dropna()
        y = self.df.loc[X.index, target_column]
        
        # Remove rows where target is NaN
        valid_indices = y.notna()
        X = X[valid_indices]
        y = y[valid_indices]
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_linear_regression(self) -> Dict:
        """
        Train a Linear Regression model.
        
        Returns:
            Dict: Training results and metrics
        """
        self.model = LinearRegression()
        self.model_type = 'regression'
        
        self.model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        # Metrics
        results = {
            'model_name': 'Linear Regression',
            'train_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                'mae': mean_absolute_error(self.y_train, y_train_pred),
                'r2_score': r2_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'mae': mean_absolute_error(self.y_test, y_test_pred),
                'r2_score': r2_score(self.y_test, y_test_pred)
            },
            'feature_importance': dict(zip(self.X_train.columns, self.model.coef_))
        }
        
        return results
    
    def train_decision_tree(self, task_type: str = 'regression', max_depth: int = 5) -> Dict:
        """
        Train a Decision Tree model.
        
        Args:
            task_type: 'regression' or 'classification'
            max_depth: Maximum depth of the tree
            
        Returns:
            Dict: Training results and metrics
        """
        if task_type == 'regression':
            self.model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
            self.model_type = 'regression'
        else:
            self.model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
            self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        if task_type == 'regression':
            results = {
                'model_name': 'Decision Tree Regressor',
                'train_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                    'mae': mean_absolute_error(self.y_train, y_train_pred),
                    'r2_score': r2_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                    'mae': mean_absolute_error(self.y_test, y_test_pred),
                    'r2_score': r2_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        else:
            results = {
                'model_name': 'Decision Tree Classifier',
                'train_metrics': {
                    'accuracy': accuracy_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'accuracy': accuracy_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        
        return results
    
    def train_random_forest(self, task_type: str = 'regression', n_estimators: int = 100, max_depth: int = 5) -> Dict:
        """
        Train a Random Forest model.
        
        Args:
            task_type: 'regression' or 'classification'
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of each tree
            
        Returns:
            Dict: Training results and metrics
        """
        if task_type == 'regression':
            self.model = RandomForestRegressor(
                n_estimators=n_estimators, 
                max_depth=max_depth, 
                random_state=42,
                n_jobs=-1
            )
            self.model_type = 'regression'
        else:
            self.model = RandomForestClassifier(
                n_estimators=n_estimators, 
                max_depth=max_depth, 
                random_state=42,
                n_jobs=-1
            )
            self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        if task_type == 'regression':
            results = {
                'model_name': 'Random Forest Regressor',
                'train_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                    'mae': mean_absolute_error(self.y_train, y_train_pred),
                    'r2_score': r2_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                    'mae': mean_absolute_error(self.y_test, y_test_pred),
                    'r2_score': r2_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        else:
            results = {
                'model_name': 'Random Forest Classifier',
                'train_metrics': {
                    'accuracy': accuracy_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'accuracy': accuracy_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        
        return results
    
    def cross_validate(self, cv: int = 5) -> Dict:
        """
        Perform cross-validation on the trained model.
        
        Args:
            cv: Number of cross-validation folds
            
        Returns:
            Dict: Cross-validation scores
        """
        if self.model is None:
            raise ValueError("No model has been trained yet")
        
        if self.model_type == 'regression':
            scoring = 'r2'
        else:
            scoring = 'accuracy'
        
        cv_scores = cross_val_score(self.model, self.X_train, self.y_train, cv=cv, scoring=scoring)
        
        return {
            'cv_scores': cv_scores.tolist(),
            'mean_cv_score': cv_scores.mean(),
            'std_cv_score': cv_scores.std()
        }
