from robaccia.wsgidispatcher import Dispatcher
from robaccia import deferred_collection

app = Dispatcher()
app.add('/{view:alnum}/[{id:unreserved}][;{noun:unreserved}]', deferred_collection)

