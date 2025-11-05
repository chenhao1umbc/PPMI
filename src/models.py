"""
Machine learning model wrappers and utilities
"""

from sklearn.linear_model import LogisticRegression as SKLogisticRegression
from sklearn.ensemble import RandomForestClassifier as SKRandomForestClassifier
from .metrics import calculate_metrics


class LogisticRegressionClassifier:
    """Wrapper for Logistic Regression with consistent interface"""

    def __init__(self, random_state=42, max_iter=1000, **kwargs):
        """
        Initialize Logistic Regression classifier

        Args:
            random_state: Random seed
            max_iter: Maximum iterations
            **kwargs: Additional arguments for LogisticRegression
        """
        self.model = SKLogisticRegression(
            random_state=random_state,
            max_iter=max_iter,
            **kwargs
        )
        self.random_state = random_state

    def fit(self, X, y):
        """Fit the model"""
        self.model.fit(X, y)
        return self

    def predict(self, X):
        """Predict labels"""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predict probabilities"""
        return self.model.predict_proba(X)

    def evaluate(self, X, y):
        """Evaluate model and return metrics"""
        y_pred = self.predict(X)
        y_prob = self.predict_proba(X)
        return calculate_metrics(y, y_pred, y_prob)


class RandomForestClassifier:
    """Wrapper for Random Forest with consistent interface"""

    def __init__(self, n_estimators=100, random_state=42, **kwargs):
        """
        Initialize Random Forest classifier

        Args:
            n_estimators: Number of trees
            random_state: Random seed
            **kwargs: Additional arguments for RandomForestClassifier
        """
        self.model = SKRandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            **kwargs
        )
        self.random_state = random_state

    def fit(self, X, y):
        """Fit the model"""
        self.model.fit(X, y)
        return self

    def predict(self, X):
        """Predict labels"""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predict probabilities"""
        return self.model.predict_proba(X)

    def evaluate(self, X, y):
        """Evaluate model and return metrics"""
        y_pred = self.predict(X)
        y_prob = self.predict_proba(X)
        return calculate_metrics(y, y_pred, y_prob)

    def feature_importances(self):
        """Get feature importances"""
        return self.model.feature_importances_


class ModelEvaluator:
    """Common evaluation pipeline for models"""

    def __init__(self, model):
        """
        Initialize evaluator

        Args:
            model: Model instance with fit, predict, predict_proba methods
        """
        self.model = model

    def train_and_evaluate(self, X_train, y_train, X_test, y_test):
        """
        Train model and evaluate on both train and test sets

        Args:
            X_train: Training features
            y_train: Training labels
            X_test: Test features
            y_test: Test labels

        Returns:
            dict: Results with train and test metrics
        """
        self.model.fit(X_train, y_train)

        train_metrics = self.model.evaluate(X_train, y_train)
        test_metrics = self.model.evaluate(X_test, y_test)

        results = {
            'train': train_metrics,
            'test': test_metrics
        }

        return results
