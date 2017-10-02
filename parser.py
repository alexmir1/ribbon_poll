from sqlalchemy.exc import IntegrityError
from app import db, app
from app.models import Color


def add_color(color):
    with app.app_context():
        db.session.add(color)
        try:
            db.session.commit()
        except IntegrityError as error:
            print(error)
        else:
            print('Successfully added color, hex: {}, image: {}'.format(color.hex, color.image_link))

if __name__ == '__main__':
    # TODO(Maksim): write parser
    add_color(Color(image_link='https://promolenta.ru/wp-content/uploads/2016/02/satin_chvetnoy--153x230.jpg',
                    hex='D7D2CB'))
