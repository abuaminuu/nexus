
---

# Nexus — Enterprise Multi-App Platform Engine

Nexus is a monolithic, multi-app Django workspace engineered to demonstrate high-throughput backend architecture, production-ready API design, and dual-authentication workflows (Session vs. JWT).

The platform encapsulates two distinct real-world applications powered by a single centralized user identity model:

1. **Commerce Engine:** A scalable e-commerce API supporting bulk inventory, optimized $N+1$-safe orders, role-based access control, and payment processing abstractions.
2. **Social Connect:** A server-rendered social network featuring friend graph management, activity feeds, post interactions, and real-time feed updates.

---

## 🏛 System Architecture

Nexus uses a modular multi-app architecture. All user identity management, role-based access control (RBAC), and authentication handling are isolated inside a dedicated `accounts` identity provider.

```text
nexus/
├── config/                 # Project configuration & root route definitions
├── accounts/               # Single Source of Truth for Auth, Roles & User Models
├── commerce/               # Headless E-Commerce REST API Engine
├── social/                 # Server-Rendered Social Network App
├── tests/                 # Cross functional tests (integration & E2E Tests)

- Overall Test Coverage 75%

```


### Key Technical Highlights

* **Centralized Identity Management:** Built around a custom user model (`accounts.User`) inheriting from `AbstractUser` with `email` as `USERNAME_FIELD`. Serves as the single source of truth across all domain apps.
* **Dual Auth Strategies:**
* **Session-Based (`django.contrib.auth`):** For server-rendered UI paths (`/social/` & `/accounts/`).
* **Stateless JWT (`djangorestframework-simplejwt`):** For headless REST API endpoints (`/api/v1/commerce/`).


* **$N+1$ Database Optimization:** Order total calculations and relation fetching delegate aggregations (`Sum`, `F` expressions) directly to PostgreSQL/MySQL engine level rather than Python runtime loops.
* **OpenAPI 3.0 Integration:** Auto-generated interactive API contracts using `drf-spectacular` and Swagger UI.

---

## 🚀 Tech Stack

| Domain | Technology / Tooling |
| --- | --- |
| **Language & Framework** | Python 3.12+, Django 5.x, Django REST Framework |
| **Authentication** | SimpleJWT (Tokens), Django Session Middleware |
| **API Documentation** | `drf-spectacular` (Swagger UI & ReDoc) |
| **Database** | PostgreSQL / MySQL / SQLite (Development) |
| **Hosting Environment** | PythonAnywhere |

---

## 📦 Data Architecture & Relationships

### `accounts` App

* **`User`**: Custom user model with role choices (`admin`, `vendor`, `customer`). Extended fields for profile media, indexing on `email`.
* **`CustomUserManager`**: Custom model manager supporting automated staff/superuser permissions on `createsuperuser`.

### `commerce` App (REST API)

* **`Product`**: Vendor-owned inventory items with stock levels, price snapshots, and availability flags.
* **`Order`**: Tracks status transitions (`pending`, `processing`, `shipped`, `delivered`, `cancelled`, `returned`) and payment reference tokens (`tx_ref`).
* **`OrderItem`**: Historical snapshot linking an `Order` to a single `Product`, protecting historical transaction data using `on_delete=models.PROTECT`.

### `social` App (Rendered Views)

* **`Post`**: User-authored content with image support and timestamp ordering.
* **`Like`**: Unique user-to-post mapping ensuring atomic like/unlike operations (`unique_together`).
* **`Friendship`**: Bi-directional relationship graph supporting connection status (`requested`, `accepted`, `blocked`).

---

## 🛠 API Endpoints Overview

Interactive Swagger documentation is available locally at `[http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)`.

### Authentication Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/auth/jwt/create/` | Obtain JWT access & refresh token pair |
| `POST` | `/api/v1/auth/jwt/refresh/` | Refresh expired access token |
| `POST` | `/accounts/login/` | HTML Session Login |
| `POST` | `/accounts/signup/` | User Account Registration |

### Commerce API

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/v1/commerce/products/` | List available products | Public |
| `POST` | `/api/v1/commerce/products/` | Create product listing | Vendor Only |
| `GET` | `/api/v1/commerce/orders/` | View user order history | Authenticated |
| `POST` | `/api/v1/commerce/orders/` | Checkout new order | Customer |

### Social App Routes

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/social/feed/` | Main activity feed |
| `POST` | `/social/posts/create/` | Create new post |
| `POST` | `/social/posts/<id>/like/` | Toggle like status on post |
| `POST` | `/social/friends/request/<user_id>/` | Send friend request |

---

## ⚡ Local Setup & Installation

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/yourusername/nexus.git
cd nexus

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Environment Variables Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_production_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3

```

### 3. Database Migration & Superuser Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create administrative user (Email required)
python manage.py createsuperuser

```

### 4. Database Seeding (Optional)

Seed the database with performant bulk data:

```bash
python manage.py shell -c "from commerce.seeds import seed_orders; seed_orders(100)"

```

### 5. Run Server

```bash
python manage.py runserver

```

Visit the application interfaces:

* **Interactive API Documentation (Swagger):** `[http://127.0.0.1:8000/api/v1.1/commece/docs/](http://127.0.0.1:8000/api/v1.1/commece/docs/)`
* **Commerce Browsable API Local:** `[http://127.0.0.1:8000/api/v1/commerce/](http://127.0.0.1:8000/api/v1.1/commerce/)`
* **Social Application local:** `[http://127.0.0.1:8000/social/](http://127.0.0.1:8000/social/)`
* **Social Application Live:** `[https://abuaminuu.pythonanywhere.com/social/](http://127.0.0.1:8000/social/)`

<!-- * **Admin Portal:** `[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)` -->

---
