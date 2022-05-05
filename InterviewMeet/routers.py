from rest_framework import routers

import users.urls
import quiz.urls
import games.urls
import resume.urls
import jobs.urls
import interviews.urls

router = routers.DefaultRouter()
router.registry.extend(users.urls.router.registry)
router.registry.extend(quiz.urls.router.registry)
router.registry.extend(games.urls.router.registry)
router.registry.extend(resume.urls.router.registry)
router.registry.extend(jobs.urls.router.registry)
router.registry.extend(interviews.urls.router.registry)

urlpatterns = router.urls