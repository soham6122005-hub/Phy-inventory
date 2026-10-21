from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_sqlalchemy import (
    SQLAlchemy
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import (
    secure_filename
)

from groq import (
    Groq
)

from dotenv import (
    load_dotenv
)

from datetime import (
    datetime,
    date,
    timedelta
)

import os


# ------------------------
# LOAD ENVIRONMENT
# ------------------------

load_dotenv()


# ------------------------
# CREATE FLASK APP
# ------------------------

app = Flask(
    __name__
)


# ------------------------
# APP CONFIGURATION
# ------------------------

app.config[
    "SECRET_KEY"
] = os.getenv(
    "SECRET_KEY",
    "change-this-pharmacy-secret-key"
)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///database.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


# ------------------------
# UPLOAD FOLDER
# ------------------------

app.config[
    "UPLOAD_FOLDER"
] = os.path.join(

    app.root_path,

    "static",

    "uploads"

)

os.makedirs(

    app.config[
        "UPLOAD_FOLDER"
    ],

    exist_ok=True

)


# ------------------------
# DATABASE
# ------------------------

db = SQLAlchemy(
    app
)


# ------------------------
# LOGIN MANAGER
# ------------------------

login_manager = LoginManager(
    app
)

login_manager.login_view = (
    "login"
)


# ------------------------
# GROQ CLIENT
# ------------------------

groq_client = Groq(

    api_key=os.getenv(
        "GROQ_API_KEY"
    )

)
# ------------------------
# USER MODEL
# ------------------------
class User(
    UserMixin,
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    mobile = db.Column(
        db.String(15)
    )

    address = db.Column(
        db.String(300)
    )

    pincode = db.Column(
        db.String(10)
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    profile_pic = db.Column(
        db.String(200),
        default="default.png"
    )
    is_admin = db.Column(
        db.Boolean,
          default=False
    )
    # User Orders

    orders = db.relationship(
        "Order",
        backref="user",
        lazy=True
    )



# ------------------------
# PRODUCT MODEL
# ------------------------

class Product(
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(50)
    )

    price = db.Column(
        db.Float
    )

    stock = db.Column(
        db.Integer
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(200),
        default="product.png"
    )

    batch_number = db.Column(
        db.String(50)
    )

    supplier = db.Column(
        db.String(150)
    )

    expiry_date = db.Column(
        db.Date
    )


# ------------------------
# ORDER MODEL
# ------------------------

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    product_name = db.Column(db.String(200))

    price = db.Column(db.Float)

    quantity = db.Column(db.Integer)

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ------------------------
# USER LOADER
# ------------------------

@login_manager.user_loader
def load_user(
    user_id
):

    return User.query.get(
        int(user_id)
    )
# ------------------------
# PRODUCT SEEDER
# ------------------------

def seed_products():
    """Seed a starter catalogue of common pharmacy inventory items."""
    if Product.query.count() > 0:
        return

    products = [
        Product(name="Paracetamol 500 mg", category="Pain Relief", price=25, stock=120,
                batch_number="PAR-2641", supplier="Cipla Ltd.",
                expiry_date=date(2027, 6, 30),
                description="Tablet strip. Store in a cool, dry place. Check pack expiry before dispensing."),
        Product(name="Cetirizine 10 mg", category="Allergy Care", price=35, stock=75,
                batch_number="CET-1187", supplier="Sun Pharma",
                expiry_date=date(2026, 11, 10),
                description="Antihistamine tablets. Dispense according to the product label and pharmacist guidance."),
        Product(name="ORS Sachets", category="Hydration", price=20, stock=100,
                batch_number="ORS-5520", supplier="FDC Ltd.",
                expiry_date=date(2027, 3, 15),
                description="Oral rehydration salts. Prepare exactly as directed on the sachet."),
        Product(name="Vitamin C 500 mg", category="Vitamins", price=90, stock=45,
                batch_number="VTC-9912", supplier="Mankind Pharma",
                expiry_date=date(2026, 10, 15),
                description="Vitamin supplement. Follow pack directions."),
        Product(name="Antiseptic Solution 100 ml", category="First Aid", price=65, stock=0,
                batch_number="ANT-3340", supplier="Dabur",
                expiry_date=date(2027, 1, 20),
                description="External-use antiseptic. Follow label directions."),
        Product(name="Adhesive Bandages", category="First Aid", price=30, stock=80,
                batch_number="BDG-7781", supplier="Johnson & Johnson",
                expiry_date=date(2027, 8, 10),
                description="Assorted adhesive dressings for minor cuts and scrapes."),
        Product(name="Digital Thermometer", category="Medical Devices", price=180, stock=18,
                batch_number="DTM-2204", supplier="Omron Healthcare",
                expiry_date=date(2028, 12, 31),
                description="Digital thermometer for temperature measurement."),
        Product(name="Cough Lozenges", category="Cough & Cold", price=40, stock=55,
                batch_number="CLG-6635", supplier="Himalaya Wellness",
                expiry_date=date(2026, 11, 5),
                description="Throat lozenges. Follow pack directions."),
        Product(name="Saline Nasal Spray", category="Cough & Cold", price=110, stock=25,
                batch_number="SNS-4471", supplier="Cipla Ltd.",
                expiry_date=date(2027, 5, 22),
                description="Saline nasal spray. Use according to label instructions."),
        Product(name="Calcium + Vitamin D", category="Vitamins", price=150, stock=0,
                batch_number="CAL-8203", supplier="Abbott",
                expiry_date=date(2026, 9, 30),
                description="Nutritional supplement. Follow pack directions."),
        Product(name="Gauze Roll", category="First Aid", price=45, stock=35,
                batch_number="GAU-1190", supplier="Birla Cellulose",
                expiry_date=date(2027, 4, 18),
                description="Sterile gauze roll for first-aid dressing."),
        Product(name="Hand Sanitizer 100 ml", category="Personal Care", price=50, stock=60,
                batch_number="HSN-9955", supplier="Dabur",
                expiry_date=date(2026, 11, 15),
                description="Hand hygiene product for external use."),
        Product(name="Surgical Masks (Pack of 10)", category="Medical Supplies", price=75, stock=50,
                batch_number="MSK-3301", supplier="3M India",
                expiry_date=date(2027, 7, 30),
                description="Disposable medical masks."),
        Product(name="Blood Glucose Test Strips", category="Medical Devices", price=350, stock=8,
                batch_number="BGT-7782", supplier="Accu-Chek (Roche)",
                expiry_date=date(2026, 10, 10),
                description="Test strips compatible with the appropriate glucose meter; check compatibility and expiry."),
        Product(name="Hot Water Bag", category="Medical Devices", price=220, stock=0,
                batch_number="HWB-5510", supplier="BPL Medical",
                expiry_date=date(2028, 6, 30),
                description="Reusable hot water bag. Follow product safety instructions."),
    ]
    db.session.add_all(products)
    db.session.commit()
    print("Pharmacy inventory seeded successfully!")


# ------------------------
# HOME
# ------------------------
@app.route("/")
def home():

    products = Product.query.limit(8).all()

    total_products = Product.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()

    low_stock_products = Product.query.filter(
        Product.stock < 10
    ).all()

    recent_orders = Order.query.order_by(
        Order.id.desc()
    ).limit(5).all()

    return render_template(
        "home.html",
        products=products,
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        low_stock=len(low_stock_products),
        low_stock_products=low_stock_products,
        recent_orders=recent_orders
    )
# ------------------------
# DASHBOARD
# ------------------------
@app.route("/dashboard")
@login_required
def dashboard():

    total_products = Product.query.count()

    total_users = User.query.count()

    total_orders = Order.query.count()

    low_stock = Product.query.filter(
        Product.stock < 10
    ).count()

    recent_orders = Order.query.order_by(
        Order.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        low_stock=low_stock,
        recent_orders=recent_orders
    )


# ------------------------
# REGISTER
# ------------------------

@app.route(
    "/register",
    methods=[
        "GET",
        "POST"
    ]
)
def register():

    if request.method == "POST":

        email = request.form[
            "email"
        ]

        existing_user = \
            User.query.filter_by(
                email=email
            ).first()

        if existing_user:

            flash(
                "Email already registered!",
                "danger"
            )

            return redirect(
                url_for(
                    "register"
                )
            )

        if request.form[
            "password"
        ] != request.form[
            "confirm_password"
        ]:

            flash(
                "Passwords do not match!",
                "danger"
            )

            return redirect(
                url_for(
                    "register"
                )
            )

        user = User(

            name=request.form[
                "name"
            ],

            email=email,

            mobile=request.form[
                "mobile"
            ],

            address=request.form[
                "address"
            ],

            pincode=request.form[
                "pincode"
            ],

            password=
            generate_password_hash(

                request.form[
                    "password"
                ]

            )
        )

        db.session.add(
            user
        )

        db.session.commit()

        flash(
            "Registration Successful!",
            "success"
        )

        return redirect(
            url_for(
                "login"
            )
        )

    return render_template(
        "register.html"
    )


# ------------------------
# LOGIN
# ------------------------

@app.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)
def login():

    if request.method == "POST":

        user = User.query.filter_by(

            email=request.form[
                "email"
            ]

        ).first()

        if user and \
            check_password_hash(

                user.password,

                request.form[
                    "password"
                ]

        ):

            login_user(
                user
            )

            flash(
                "Welcome Back!",
                "success"
            )

            if user.is_admin:

                today = date.today()
                expiry_threshold = today + timedelta(days=30)

                expired = Product.query.filter(
                    Product.expiry_date.isnot(None),
                    Product.expiry_date < today
                ).count()

                expiring_soon = Product.query.filter(
                    Product.expiry_date.isnot(None),
                    Product.expiry_date >= today,
                    Product.expiry_date <= expiry_threshold
                ).count()

                out_of_stock = Product.query.filter(
                    Product.stock <= 0
                ).count()

                if expired or expiring_soon or out_of_stock:
                    flash(
                        "📋 You have pending inventory alerts — "
                        "check the admin panel for details.",
                        "warning"
                    )

                return redirect(
                    url_for(
                        "admin_panel"
                    )
                )

            return redirect(
                url_for(
                    "dashboard"
                )
            )

        flash(
            "Invalid Email or Password!",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ------------------------
# LOGOUT
# ------------------------

@app.route(
    "/logout"
)
@login_required
def logout():

    logout_user()

    flash(
        "Logged Out Successfully!",
        "info"
    )

    return redirect(
        url_for(
            "home"
        )
    )
# ------------------------
# PRODUCTS
# ------------------------
from sqlalchemy import or_

@app.route("/products")
def products():

    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "")

    query = Product.query

    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.category.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    pagination = query.order_by(Product.id.desc()).paginate(
        page=page,
        per_page=9,
        error_out=False
    )

    return render_template(
        "products.html",
        products=pagination.items,
        pagination=pagination,
        search=search
    )


# ------------------------
# PLACE ORDER
# ------------------------

@app.route(
    "/place_order/<int:product_id>"
)
@login_required
def place_order(
    product_id
):

    product = \
        Product.query.get_or_404(
            product_id
        )

    # Check Stock

    if product.stock <= 0:

        flash(
            "Product is Out of Stock!",
            "danger"
        )

        return redirect(
            url_for(
                "products"
            )
        )

    # Create Order

    order = Order(

        product_name=
        product.name,

        price=
        product.price,

        quantity=1,

        user_id=
        current_user.id

    )

    # Reduce Stock

    product.stock -= 1

    db.session.add(
        order
    )

    db.session.commit()

    flash(
        "Order Placed Successfully!",
        "success"
    )

    return redirect(
        url_for(
            "orders"
        )
    )


# ------------------------
# ORDERS
# ------------------------
@app.route("/order/<int:product_id>", methods=["GET", "POST"])
@login_required
def order(product_id):

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":

        quantity = int(request.form["quantity"])

        if quantity > product.stock:
            flash("Insufficient Stock!", "danger")
            return redirect(
                url_for("order", product_id=product.id)
            )

        new_order = Order(
            user_id=current_user.id,
            product_name=product.name,
            price=product.price,
            quantity=quantity,
            status="Pending"
        )

        db.session.add(new_order)

        product.stock -= quantity

        db.session.commit()

        flash("Order Placed Successfully!", "success")

        return redirect(url_for("orders"))

    return render_template(
        "order.html",
        product=product
    )
@app.route("/orders")
@login_required
def orders():

    user_orders = Order.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "orders.html",
        orders=user_orders,
        total_orders=len(user_orders),
        pending_orders=len(
            [o for o in user_orders if o.status == "Pending"]
        ),
        completed_orders=len(
            [o for o in user_orders if o.status == "Completed"]
        )
    )
@app.route("/cancel_order/<int:order_id>")
@login_required
def cancel_order(order_id):

    order = Order.query.get_or_404(order_id)
    order.status = "Cancelled"

    db.session.commit()

    flash("Order Cancelled Successfully!", "success")
    return redirect(url_for("orders"))
# ------------------------
# PROFILE
# ------------------------
@app.route("/profile")
@login_required
def profile():

    total_products = Product.query.count()

    total_orders = Order.query.filter_by(
        user_id=current_user.id
    ).count()

    total_sales = db.session.query(
        db.func.sum(Order.price * Order.quantity)
    ).filter(
        Order.user_id == current_user.id
    ).scalar() or 0

    return render_template(
        "profile.html",
        total_products=total_products,
        total_orders=total_orders,
        total_sales=total_sales
    )
@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def profile_edit():

    if request.method == "POST":

        current_user.name = request.form["name"]
        current_user.email = request.form["email"]
        current_user.mobile = request.form["mobile"]
        current_user.address = request.form["address"]
        current_user.pincode = request.form["pincode"]

        password = request.form.get("password")

        if password:
            current_user.password = generate_password_hash(password)

        # Profile Photo Upload
        file = request.files.get("profile_pic")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            current_user.profile_pic = filename

        db.session.commit()

        flash("Profile Updated Successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile_edit.html")



# ------------------------
# AI CHAT
# ------------------------

@app.route(
    "/ai_chat",
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def ai_chat():

    question = ""
    answer = ""

    if request.method == "POST":

        question = request.form[
            "question"
        ]

        try:

            response = \
                groq_client.chat.completions.create(

                    model=
                    "llama-3.3-70b-versatile",

                    messages=[

                        {
                            "role":
                            "system",

                            "content":

                            """
                            You are an AI Pharmacy
                            Assistant for a
                            Pharmacy Inventory
                            Management System.

                            Help users with:

                            - Medicine Recommendations
                            - Medicine Comparisons
                            - Dosage & Usage Guidance
                            - Expiry & Storage Advice
                            - Pharmacy & Health Questions

                            Always remind users to
                            consult a doctor or
                            pharmacist for medical
                            advice before taking
                            any medicine.
                            """
                        },

                        {
                            "role":
                            "user",

                            "content":
                            question
                        }

                    ]

                )

            answer = \
                response.choices[
                    0
                ].message.content

        except Exception as e:

            answer = \
                f"Error: {e}"

    return render_template(

        "ai_chats.html",

        question=
        question,

        answer=
        answer

    )
from sqlalchemy import or_

@app.route("/search")
def search():

    query = request.args.get("q", "")

    products = Product.query.filter(

        or_(

            Product.name.ilike(f"%{query}%"),

            Product.category.ilike(f"%{query}%"),

            Product.description.ilike(f"%{query}%")

        )

    ).all()

    return render_template(

        "search.html",

        products=products,

        query=query

    )
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admin")
@login_required
def admin_panel():

    if not current_user.is_admin:
        flash("Access Denied!", "danger")
        return redirect(url_for("dashboard"))

    total_products = Product.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()

    low_stock_products = Product.query.filter(
        Product.stock < 10
    ).all()

    # Out-of-stock medicines (stock is zero or less)
    out_of_stock_products = Product.query.filter(
        Product.stock <= 0
    ).all()

    # Expiry alerts — already expired or expiring within 30 days
    today = date.today()
    expiry_threshold = today + timedelta(days=30)

    expired_products = Product.query.filter(
        Product.expiry_date.isnot(None),
        Product.expiry_date < today
    ).all()

    expiring_soon_products = Product.query.filter(
        Product.expiry_date.isnot(None),
        Product.expiry_date >= today,
        Product.expiry_date <= expiry_threshold
    ).all()

    # Count of active alerts for the notification badge
    alert_count = (
        len(out_of_stock_products)
        + len(expired_products)
        + len(expiring_soon_products)
    )

    total_sales = 0

    orders = Order.query.all()

    for order in orders:
        total_sales += order.price * order.quantity

    recent_orders = Order.query.order_by(
        Order.id.desc()
    ).limit(10).all()

    users = User.query.all()

    # Flash notices to the admin about expiring or out-of-stock medicines
    if out_of_stock_products:
        names = ", ".join(p.name for p in out_of_stock_products)
        flash(
            f"⚠️ {len(out_of_stock_products)} medicine(s) out of stock: {names}",
            "danger"
        )
    if expired_products:
        names = ", ".join(p.name for p in expired_products)
        flash(
            f"🚫 {len(expired_products)} medicine(s) expired: {names}",
            "danger"
        )
    if expiring_soon_products:
        names = ", ".join(p.name for p in expiring_soon_products)
        flash(
            f"⏰ {len(expiring_soon_products)} medicine(s) expiring within 30 days: {names}",
            "warning"
        )

    return render_template(
        "admin.html",
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        low_stock_products=low_stock_products,
        out_of_stock_products=out_of_stock_products,
        expired_products=expired_products,
        expiring_soon_products=expiring_soon_products,
        alert_count=alert_count,
        total_sales=total_sales,
        recent_orders=recent_orders,
        users=users
    )
@app.route("/admin/products")
@login_required
def admin_products():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    products = Product.query.all()

    today = date.today()
    expiry_threshold = today + timedelta(days=30)

    expired_count = Product.query.filter(
        Product.expiry_date.isnot(None),
        Product.expiry_date < today
    ).count()

    expiring_soon_count = Product.query.filter(
        Product.expiry_date.isnot(None),
        Product.expiry_date >= today,
        Product.expiry_date <= expiry_threshold
    ).count()

    return render_template(
        "admin_products.html",
        products=products,
        today=today,
        expiry_threshold=expiry_threshold,
        expired_count=expired_count,
        expiring_soon_count=expiring_soon_count
    )
@app.route("/admin/users")
@login_required
def admin_users():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    users = User.query.all()

    return render_template(
        "admin_user.html",
        users=users
    )
@app.route("/admin/orders")
@login_required
def admin_orders():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    orders = Order.query.order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "admin_orders.html",
        orders=orders
    )
@app.route("/admin/delete_product/<int:id>")
@login_required
def delete_product(id):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    flash(
        "Product Deleted Successfully",
        "success"
    )

    return redirect(
        url_for("admin_products")
    )
@app.route("/admin/order_status/<int:id>/<status>")
@login_required
def order_status(id, status):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    order = Order.query.get_or_404(id)

    order.status = status

    db.session.commit()

    flash(
        "Order Status Updated",
        "success"
    )

    return redirect(
        url_for("admin_orders")
    )
@app.route("/admin/add_product", methods=["GET", "POST"])
@login_required
def add_product():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        expiry_raw = request.form.get("expiry_date", "")

        product = Product(
            name=request.form["name"],
            category=request.form["category"],
            price=float(request.form["price"]),
            stock=int(request.form["stock"]),
            description=request.form["description"],
            batch_number=request.form.get("batch_number") or None,
            supplier=request.form.get("supplier") or None,
            expiry_date=(
                datetime.strptime(
                    expiry_raw, "%Y-%m-%d"
                ).date()
                if expiry_raw else None
            )
        )

        db.session.add(product)
        db.session.commit()

        flash("Medicine Added Successfully", "success")

        return redirect(url_for("admin_products"))

    return render_template("add_product.html")
@app.route("/admin/edit_product/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        expiry_raw = request.form.get("expiry_date", "")

        product.name = request.form["name"]
        product.category = request.form["category"]
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])
        product.description = request.form["description"]
        product.batch_number = request.form.get("batch_number") or None
        product.supplier = request.form.get("supplier") or None
        product.expiry_date = (
            datetime.strptime(
                expiry_raw, "%Y-%m-%d"
            ).date()
            if expiry_raw else None
        )

        db.session.commit()

        flash(
            "Medicine Updated Successfully",
            "success"
        )

        return redirect(
            url_for("admin_products")
        )

    return render_template(
        "edit_product.html",
        product=product
    )
@app.route("/admin/delete_user/<int:id>")
@login_required
def delete_user(id):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(id)

    if user.is_admin:
        flash("Admin Account Cannot Be Deleted", "danger")
        return redirect(url_for("admin_users"))

    db.session.delete(user)
    db.session.commit()

    flash("User Deleted Successfully", "success")

    return redirect(url_for("admin_users"))
# ------------------------
# USER LOADER
# ------------------------

@login_manager.user_loader
def load_user(
    user_id
):

    return User.query.get(
        int(user_id)
    )
def create_admin():

    admin = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    if not admin:

        admin = User(
            name="Administrator",
            email="admin@gmail.com",
            mobile="9999999999",
            address="Admin Office",
            pincode="000000",
            password=generate_password_hash("admin123"),
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully!")

    else:

        admin.is_admin = True
        db.session.commit()

with app.app_context():

    db.create_all()

    seed_products()

    create_admin()


# Apply a consistent pharmacy-themed palette to existing HTML templates.
@app.after_request
def pharmacy_theme(response):
    if response.mimetype == "text/html":
        theme = """
<style id="pharmacy-theme">
:root{--pharmacy:#087f8c;--pharmacy-dark:#075b63;--mint:#e8f7f4;--accent:#f4b942;--ink:#20313b;--surface:#ffffff}
body{background:#f3f8fa!important;color:var(--ink)}
nav,.navbar,header,.sidebar{background:linear-gradient(135deg,var(--pharmacy-dark),var(--pharmacy))!important}
a{color:var(--pharmacy)}
.btn-primary,button[type=submit],input[type=submit]{background:var(--pharmacy)!important;border-color:var(--pharmacy)!important;color:#fff!important;border-radius:9px}
.btn-primary:hover,button[type=submit]:hover,input[type=submit]:hover{background:var(--pharmacy-dark)!important}
.card,.table-responsive,.product-card,.stat-card{border:1px solid #dcebea!important;border-radius:14px!important;box-shadow:0 6px 20px rgba(7,91,99,.08)!important}
.card-header{background:var(--mint)!important;color:var(--pharmacy-dark)!important}
.table thead th{background:var(--pharmacy-dark)!important;color:#fff!important}
.badge-success,.text-success{color:#087f5b!important}
input,select,textarea{border-radius:8px!important;border-color:#cbdcde!important}
</style>"""
        body = response.get_data(as_text=True)
        if "</head>" in body.lower():
            index = body.lower().find("</head>")
            body = body[:index] + theme + body[index:]
            response.set_data(body)
    return response


# ------------------------
# RUN APPLICATION
# ------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )