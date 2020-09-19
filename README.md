# Best Habr API

Best Habr API is an aggregator of the best articles from <code><a href="https://habr.com/ru">habr</a></code> per day.

<h2>
	Features
</h2>
<ul>
	<li>
		Parses articles from <code><a href="https://habr.com/ru">Habr</a></code> once a day;
	</li>
	<li>
		Include two endpoints:
		<ul>
			<li>
			List of articles;
			</li>
			<li>
			Article details.
			</li>
		</ul>
	</li>
</ul>

<h2>Installation</h2>

<h5>
	Required version:
</h5>
<ul>
	<li>
		Python 3.8;
	</li>
	<li>
		Django 3.1.1
	</li>
</ul>

<p>
    Clone repository.
</p>
<pre>
<code>
git clone https://github.com/block2busted/best_habr_api.git
cd best_habr_api
</code>
</pre>

<p>
Add virtual environment and activate it.
</p>
<pre>
<code>
python3 -m venv best_habr_api-env
# On Windows, run:
best_habr_api-env\Scripts\activate.bat
# On Unix or MacOS, run:
source best_habr_api-env/bin/activate
</code>
</pre>

<p>
	Install requirements.
</p>

<pre>
<code>
pip install -r requirements.txt
</code>
</pre>

<h2>
Usage API.
</h2>

<p>
	Run migrations before running the server.
</p>
<pre>
<code>
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
</code>
</pre>

<p>
	If you want to test the parser right now, change value <code>CELERY_PARSE_TASK_SCHEDULE</code> in settings.py:
</p>
<pre>
<code>
CELERY_PARSE_TASK_SCHEDULE = crontab(minute=0, hour=0)  
# default parse at 00:00. Put value 60 and parser will run every 60 seconds.
CELERY_PARSE_TASK_SCHEDULE = 60
</code>
</pre>

<p>
	Test your redis-connection and run celery-beat on second terminal window.
</p>
<pre>
<code>
redis-cli ping
# PONG
celery -A best_habr_api beat -l info
</code>
</pre>

<p>
	You can start the worker in the foreground by executing the command in third terminal window:
</p>
<pre>
<code>
celery -A best_habr_api worker -l info
</code>
</pre>

<h2>
	Logging
</h2>
<p>
	If any errors occur during parsing, you can view the logs in log directory:
</p>

<code>
	/best_habr_api/best_habr_api/logs
</code>
