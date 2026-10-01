import os
import sys
import random
from faker import Faker

# Get the current directory and parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add both current and parent directories to the path
sys.path.append(parent_dir)
sys.path.append(current_dir)

# Get the current directory and parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from snippets folder

# Add the project root to sys.path
sys.path.insert(0, project_root)

# 1. SET THE SETTINGS MODULE (Crucial)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. INITIALIZE DJANGO
import django
django.setup()

# Now import Django models AFTER setup
from accounts.models import User

fake = Faker("en_NG")

def seed_fake_customers(records):
    
    for i in range(records):
        try:
            # to check if no existing record
            username = fake.user_name()
            email = f"{username}@example.com"

            # check if user exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=email,
                password="password",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=random.choice(['customer'])
            )
            user.save()
        except Exception as e:
            print(f"err creating user {e}")
            continue
            
    print(f"{records} realistic entries generated.")

def seed_fake_vendors(records):
    
    for i in range(records):
        try:
            # to check if no existing record
            username = fake.user_name()
            email = f"{username}@example.com"

            # check if user exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=email,
                password="password",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role="vendor"
            )
            user.save()
        except Exception as e:
            print(f"err creating user {e}")
            continue
            
    print(f"{records} realistic entries generated.")

def seed_fake_friends(records):
    pass

def gen_sample_data(n):
    for _ in range(n):
        print(fake.ecommerce_category(), fake.ecommerce_price())
        # print(fake.first_name(), fake.ecommerce_name(), fake.ecommerce_category(), fake.ecommerce_price())

    id = [1,3,2]
    # print(random.choice(id))


if __name__ == "__main__":
    # run main
    # gen_sample_data(15)
    # seed_fake_customers(3)
    # seed_fake_vendors(2)
    pass
