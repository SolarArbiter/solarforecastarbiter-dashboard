from flask_dance.consumer.storage.sqla import (
    OAuthConsumerMixin, SQLAlchemyStorage)
from flask_sqlalchemy import SQLAlchemy


from sfa_dash.blueprints.auth0 import current_user


db = SQLAlchemy()


class OAuth(OAuthConsumerMixin, db.Model):
    user = db.Column(db.String(24))


session_storage = SQLAlchemyStorage(OAuth, db.session,
                                    user_required=True,
                                    user=current_user)
