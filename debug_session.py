from app import app as flask_app

# simple test script to login and print session
with flask_app.test_client() as client:
    resp = client.post('/login', data={'username':'johnhmoore01@gmail.com','password':'password123'})
    print('login status', resp.status_code, 'location', resp.location)
    with client.session_transaction() as sess:
        print('session keys', list(sess.keys()))
        print('session data', dict(sess))
