from database import db

mediums = {'film', 'audio', 'literature', 'other'}
medium_type = db.Enum(*mediums, name='medium_type', validate_strings=True)

consumed_states = {'not started', 'started', 'finished'}
consumed_state_type = db.Enum(*consumed_states, name='consumed_state_type', validate_strings=True)


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column('id', db.Integer, primary_key=True)
    medianame = db.Column('medianame', db.String(80))
    user = db.Column('user', db.Integer, db.ForeignKey('users.id'))
    medium = db.Column('medium', medium_type, default='other')
    consumed_state = db.Column('consumed_state', consumed_state_type, default='not started')
    description = db.Column('description', db.String(500))
    order = db.Column('order', db.Integer, default=0)

    def __init__(self, medianame, userid, medium='other', consumed_state='not started', description='', order=0):
        if medium not in mediums:
            raise ValueError('medium must be one of these values: {}'.format(mediums))
        if consumed_state not in consumed_states:
            raise ValueError('consumed_state must be on of these values: {}'.format(consumed_states))

        self.medianame = medianame
        self.user = userid
        self.medium = medium
        self.consumed_state = consumed_state
        self.description = description
        self.order = order

    def __repr__(self):
        return '<Media(id={}, medianame={}, user={}, medium={}, consumed_state={}, order={})>'.format(
            self.medianame, self.user, self.medium, self.consumed_state, self.order)

    def as_dict(self):
        """
        returns a dict representing this media element. Used when returning media data as json in response
        """
        return {
            'id': self.id,
            'name': self.medianame,
            'medium': self.medium,
            'consumed_state': self.consumed_state,
            'description': self.description,
            'order': self.order
        }
