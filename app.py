import streamlit as st
from models import User
from datetime import datetime
import os
import base64
from fpdf import FPDF

# ------------------ MENU ITEMS ------------------
menu_items = [
    {"name": "Coffee", "price": 80, "image": "Coffee.jfif"},
    {"name": "Veg Roll", "price": 60, "image": "Veg_Roll.jfif"},
    {"name": "Pizza", "price": 250, "image": "Pizza.jfif"},
    {"name": "Burger", "price": 120, "image": "burger.jpg"},
    {"name": "Pasta", "price": 180, "image": "Pasta.jfif"},
    {"name": "French Fries", "price": 90, "image": "fries.jpg"},
    {"name": "Samosa", "price": 40, "image": "samosa.jpg"},
    {"name": "Cold Drink", "price": 50, "image": "cold_drink.jpg"},
    {"name": "Tea", "price": 40, "image": "tea.jpg"},
    {"name": "Sandwich", "price": 100, "image": "sandwich.jpg"},
    {"name": "Idli", "price": 60, "image": "idli.jpg"},
    {"name": "Dosa", "price": 80, "image": "dosa.jpg"},
    {"name": "Paneer Tikka", "price": 200, "image": "paneer_tikka.jpg"},
    {"name": "Momos", "price": 110, "image": "momos.jpg"},
    {"name": "Biryani", "price": 220, "image": "biryani.jpg"},
    {"name": "Juice", "price": 70, "image": "juice.jpg"},
    {"name": "Ice Cream", "price": 90, "image": "ice_cream.jpg"},
    {"name": "Soup", "price": 100, "image": "soup.jpg"},
    {"name": "Chole Bhature", "price": 150, "image": "chole_bhature.jpg"},
    {"name": "Pav Bhaji", "price": 120, "image": "pav_bhaji.jpg"},
]

# ------------------ STREAMLIT CONFIG ------------------
st.set_page_config(page_title="ThreeSpice Bistro", page_icon="🍴", layout="centered")

# ------------------ SESSION SETUP ------------------

if "user" not in st.session_state:
    st.session_state.user = None
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "invoice" not in st.session_state:
    st.session_state.invoice = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# ------------------ FUNCTIONS ------------------
def go_to(page):
    st.session_state.page = page

def add_to_cart(item):
    if item["name"] in st.session_state.cart:
        st.session_state.cart[item["name"]]["qty"] += 1
    else:
        st.session_state.cart[item["name"]] = {"price": item["price"], "qty": 1}

def remove_from_cart(item):
    if item["name"] in st.session_state.cart:
        if st.session_state.cart[item["name"]]["qty"] > 1:
            st.session_state.cart[item["name"]]["qty"] -= 1
        else:
            del st.session_state.cart[item["name"]]

def add_item(name, price):
        add_to_cart({"name": name, "price": price})

def remove_item(name):
    remove_from_cart({"name": name})

def logout():
    st.session_state.user = None
    st.session_state.cart = {}
    st.session_state.page = "home"

#-------------------BG FRONT-------------------------

def set_bg_image(image_path):
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("data:image/png;base64,{data}") center/cover no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------ HOME PAGE ------------------

if st.session_state.page == "home":
    set_bg_image("images/restaurant_banner.jpg")   # Background Image

    st.markdown("<h1 style='color:white;'>🍽️ Welcome to ThreeSpice Bistro..</h1>", unsafe_allow_html=True)
    st.write("<p style='color:white; text-align:center;'>Experience delicious food at your fingertips.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        login = st.button("👤 User Login", use_container_width=True)
        register = st.button("📝 New User? Register", use_container_width=True)

    if login:
        go_to("login")
    if register:
        go_to("register")

# ------------------ REGISTER PAGE ------------------
elif st.session_state.page == "register":
    st.subheader("Register Yourself 📝")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    if st.button("Register"):
        if "@" not in email:
            st.error("❌ Please enter a valid email address containing '@'")
        else:
            try:
                user = User(username, password, email)
                user.save()
                st.success("✅ Registered successfully! Please login.")
                go_to("login")
            except Exception:
                st.error("❌ Username already exists.")

    if st.button("⬅️ Back to Home"):
        go_to("home")

# ------------------ LOGIN PAGE ------------------
elif st.session_state.page == "login":
    st.subheader("User Login 👤")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = User.get_user(username, password)
        if user:
            st.session_state.user = user
            st.success(f"✅ Welcome, {username}!  Wallet: ₹{user[5]:.2f}")
            go_to("menu")
        else:
            st.error("❌ Invalid credentials.")

    if st.button("⬅️ Back"):
        go_to("home")

#---------------------  MENU PAGE --------------------------------
                    
elif st.session_state.page == "menu":
    
    st.title("🍴 Menu")
    st.write("Select your favorite dishes and add them to your cart.")

    for item in menu_items:
        with st.container():  # ensures each item stays in one row
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                image_path = os.path.join("images", item["image"])
                if os.path.exists(image_path):
                    st.image(image_path, width=110)
                else:
                    st.write("[No image]")

            with col2:
                st.subheader(item["name"])
                st.write(f"💰 ₹{item['price']}")

            with col3:
                col_plus, col_qty, col_minus = st.columns([1, 1, 1])

                with col_plus:
                    st.button(
                        "➕",
                        key=f"add_{item['name']}",
                        on_click=add_item,
                        args=(item["name"], item["price"])
                    )

                with col_qty:
                    qty = st.session_state.cart.get(item["name"], {}).get("qty", 0)
                    st.markdown(f"<h5 style='text-align:center;margin-top:5px;'>{qty}</h5>", unsafe_allow_html=True)
                with col_minus:
                    st.button(
                        "➖",
                        key=f"remove_{item['name']}",
                        on_click=remove_item,
                        args=(item["name"],)
                    )

        st.markdown("---")  # add separator between items

    # --------- Cart Summary --------------
    if st.session_state.cart:
        st.subheader("🛒 Cart Summary")
        total = sum(v["price"] * v["qty"] for v in st.session_state.cart.values())

        for item, details in st.session_state.cart.items():
            st.write(f"{item} x {details['qty']} = ₹{details['price'] * details['qty']}")

        st.write(f"**Total: ₹{total}**")

        if st.button("Proceed to Checkout ✅"):
            go_to("checkout")

    else:
        st.info("Your cart is empty.")
    
#------------------ checkout page ---------------------------
elif st.session_state.page == "checkout":
    st.title("🧾 Checkout")
    st.write("Review your order before confirming:")
    
# ---------------- CART ITEMS WITH EXPANDERS ----------------
    for item_name, details in st.session_state.cart.items():
        price = details['price']
        qty = details['qty']
        total = price * qty

        with st.expander(f"{item_name} — ₹{price} x {qty} = ₹{total}"):
            st.write(f"**Price per item:** ₹{price}")
            st.write(f"**Quantity:** {qty}")
            st.write(f"**Subtotal:** ₹{total}")

    # ---------------- TOTAL ----------------
    total_amount = sum(v["price"] * v["qty"] for v in st.session_state.cart.values())
    st.markdown(f"### 💰 Total Amount: ₹{total_amount}")

    # ---------------- USER WALLET ----------------
    user = None
    if st.session_state.user:
        user = User.get_user_by_id(st.session_state.user[0])
        wallet = user[5]
        visit_count = user[4]
        st.info(f"Wallet Balance: ₹{wallet:.2f}")
    else:
        st.warning("Login required for payment.")
        st.stop()

    # ---------------- DISCOUNT LOGIC (4th visit = 10%) ----------------
    discount = 0.1 * total_amount if visit_count % 4 == 3 else 0
    final_amount = total_amount - discount

    st.markdown(f"### 🎯 Discount: {discount}")
    st.markdown(f"### ✅ Final Payable Amount: {final_amount}")

    
    if st.button("✅ Confirm Order"):
        if wallet < final_amount:
            st.error("❌ Not enough wallet balance.")
        else:
            # Deduct wallet
            new_wallet = wallet - final_amount
            User.update_wallet(user[0], new_wallet)

            # Create invoice dictionary
            st.session_state.invoice = {
                "items": st.session_state.cart,
                "total": total_amount,
                "discount": discount,
                "final": final_amount,
                "wallet_after": new_wallet,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            st.success("🎉 Order placed successfully!")
            st.balloons()
           
#--------------------------INVOICE generation----------------
            
            inv = st.session_state.invoice
            st.divider()
            st.subheader("🧾 Invoice")  
            st.write(f"Date: {inv['date']}")
            st.write("### Items:")

            for item, d in inv["items"].items():
                st.write(f"- {item}: {d['qty']} × Rs. {d['price']}")

            st.write(f"### Total: Rs. {inv['total']}")
            st.write(f"### Discount: Rs. {inv['discount']}")
            st.write(f"### Final Payable: Rs. {inv['final']}")
            st.write(f"### Wallet After Payment: Rs. {inv['wallet_after']}")


            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, "ThreeSpice Bistro - Invoice", ln=True, align="C")
            pdf.ln(5)
            pdf.cell(200, 10, f"Date: {inv['date']}", ln=True)
            pdf.ln(5)

            for item, d in inv["items"].items():
                pdf.cell(200, 10, f"{item}: {d['qty']} x Rs. {d['price']}", ln=True)

            pdf.ln(5)
            pdf.cell(200, 10, f"Total: Rs. {inv['total']}", ln=True)
            pdf.cell(200, 10, f"Discount: Rs. {inv['discount']}", ln=True)
            pdf.cell(200, 10, f"Final Payable: Rs. {inv['final']}", ln=True)
            pdf.cell(200, 10, f"Wallet After Payment: Rs. {inv['wallet_after']}", ln=True)

            pdf.output("Invoice.pdf")

            # Show download button immediately
            with open("Invoice.pdf", "rb") as f:
                st.download_button("⬇ Download Your Invoice", f, file_name="Invoice.pdf")

            # Clear cart after generating invoice
            st.session_state.cart = {}

    st.markdown("---")

    # ------------- LOGOUT BUTTON -------------
    if st.button("🔒 Logout"):
        logout()
        st.success("You have been logged out!") 

