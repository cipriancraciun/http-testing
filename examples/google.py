

import httt


_tests = httt.tests ("main")


_requests = _tests.requests () .with_endpoint ("https:www.google.com:443")
_www_requests = _requests.with_host ("www.google.com")


_responses = _tests.responses ()
_response_200_with_body = _responses.fork () .expect_200 () .has_body ()




_tests.test (
		"www-redirect",
		_requests.with_host ("google.com") .with_path ("/"),
		_responses.fork () .redirect_to ("https://www.google.com/"),
	)

_tests.test (
		"https-get-/",
		_www_requests.with_path ("/"),
		_response_200_with_body,
	)




_tests.execute ()

