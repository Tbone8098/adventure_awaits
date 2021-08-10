from flask_app import app
from flask_app.controllers import controller_routes, controller_user, controller_admin_routers, controller_family, controller_category, controller_post, controller_img

if __name__=="__main__":
    app.run(debug=True)