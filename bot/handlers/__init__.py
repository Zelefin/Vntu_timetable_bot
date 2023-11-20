from .delete_me import delete_me_router
from .desing import design_router
from .registration import registration_router
from .start import start_router
from .mailing import mailing_router
from .feedback import feedback_router
from .update_timetable import update_timetable_router
from .donate import donate_router
from .links import links_router
from .presidents import presidents_router
from .profile import profile_router
from .inline_mode import inline_router


__all__ = ['routers']

routers = (start_router, registration_router, design_router, delete_me_router, mailing_router, feedback_router,
           update_timetable_router, donate_router, links_router, presidents_router, profile_router, inline_router)
