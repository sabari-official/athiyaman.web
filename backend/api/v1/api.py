from fastapi import APIRouter
from backend.modules.auth.router import router as auth_router
from backend.modules.applications.router import router as applications_router
from backend.modules.profiles.router import router as profiles_router
from backend.modules.teams.router import router as teams_router
from backend.modules.referrals.router import router as referrals_router
from backend.modules.levels.router import router as levels_router
from backend.modules.waste.router import router as waste_router
from backend.modules.collection_centers.router import router as centers_router
from backend.modules.claims.router import router as claims_router
from backend.modules.payments.router import router as payments_router
from backend.modules.notifications.router import router as notifications_router
from backend.modules.audit.router import router as audit_router
from backend.modules.analytics.router import router as analytics_router
from backend.modules.location.router import router as location_router

api_router = APIRouter()

# Mount feature routers
api_router.include_router(auth_router)
api_router.include_router(applications_router)
api_router.include_router(profiles_router)
api_router.include_router(teams_router)
api_router.include_router(referrals_router)
api_router.include_router(levels_router)
api_router.include_router(waste_router)
api_router.include_router(centers_router)
api_router.include_router(claims_router)
api_router.include_router(payments_router)
api_router.include_router(notifications_router)
api_router.include_router(audit_router)
api_router.include_router(analytics_router)
# Remove the prefix from location_router here, we already added it in the router definition
api_router.include_router(location_router)


