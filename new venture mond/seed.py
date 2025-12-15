from database import SessionLocal, engine
import models
import auth

# Initialize DB
db = SessionLocal()

def seed_users():
    print("Seeding database...")
    
    # 1. Create Admin User
    admin_email = "admin@venturemond.com"
    admin = db.query(models.User).filter(models.User.email == admin_email).first()
    if not admin:
        print(f"Creating admin user: {admin_email}")
        hashed_pwd = auth.get_password_hash("admin123")
        admin_user = models.User(
            email=admin_email,
            hashed_password=hashed_pwd,
            full_name="Admin User",
            role="admin"
        )
        db.add(admin_user)
    else:
        print("Admin user already exists.")

    # 2. Create Client User
    client_email = "client@venturemond.com"
    client = db.query(models.User).filter(models.User.email == client_email).first()
    if not client:
        print(f"Creating client user: {client_email}")
        hashed_pwd = auth.get_password_hash("client123")
        client_user = models.User(
            email=client_email,
            hashed_password=hashed_pwd,
            full_name="Client User",
            role="client"
        )
        db.add(client_user)
        db.commit() # Commit to get ID
        db.refresh(client_user)
        
        # Create Profile
        print("Creating client profile...")
        profile = models.ClientProfile(
            user_id=client_user.id,
            company_name="Venturemond Demo Corp",
            project_name="Dashboard Redesign",
            budget="$15k",
            status="Active"
        )
        db.add(profile)
    else:
        print("Client user already exists.")

    db.commit()
    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed_users()
