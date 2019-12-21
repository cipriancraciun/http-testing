

import httt


_tests = httt.tests ("google")
_tests.requests_shared.with_endpoint ("https:www3.l.google.com:443")
_tests.responses_shared.has_header ("server", "gws") .has_header ("date") .has_header ("alt-svc")


_tests.new (
		"apex-to-www-redirect",
		_tests.requests.with_host ("google.com"),
		_tests.responses.redirect_to ("https://www.google.com/"),
	)

_tests.new (
		"www-get-/",
		_tests.requests.with_host ("www.google.com"),
		_tests.responses.expect_200 () .has_body (),
	)


_tests.execute ()

