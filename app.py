from flask import Flask
from apis import api
from common.scheduler import SchedulerConfig
app = Flask(__name__)
scheduler = SchedulerConfig().scheduler
scheduler.init_app(app)
scheduler.start()
api.init_app(app)
app.run(debug=True,host="0.0.0.0", port=5001)