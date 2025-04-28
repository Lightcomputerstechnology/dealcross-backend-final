from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url="postgres://dealcross_db_mybg_user:your_password@dpg-d06rhgali9vc73elmnlg-a/dealcross_db_mybg",
        modules={"models": ["models.user", "models.kyc", "models.wallet", "models.admin_wallet", 
                            "models.deal", "models.share", "models.escrow_tracker", 
                            "models.dispute", "models.settings", "models.aiinsight"]}
    )
    await Tortoise.generate_schemas()  # Auto-create tables if they don't exist

async def close_db():
    await Tortoise.close_connections()