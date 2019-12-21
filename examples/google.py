

from httt import tests, chain


_tests = tests (
		"google",
		requests = chain.with_endpoint ("https:www3.l.google.com:443"),
		responses = chain
				.has_header ("server", "gws")
				.has_header ("date")
				.has_header ("alt-svc"),
		debug = True,
	)


_tests.new (
		"apex-to-www-redirect",
		requests = chain.with_host ("google.com"),
		responses = chain.redirect_to ("http://www.google.com/"),
	)

_tests.new (
		"www-get-/",
		requests = chain.with_host ("www.google.com"),
		responses = chain.expect_200 () .has_body (),
	)


_tests.execute ()

