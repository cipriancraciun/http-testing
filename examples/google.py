

from httt import tests, chain
import sys


_tests = tests (
		identifier = "google",
		requests = chain
				.with_endpoint ("https:www3.l.google.com:443")
				.with_header ("User-Agent", "HTTT"),
		responses = chain
				.has_header ("server", "gws")
				.has_header ("date")
				.has_header ("alt-svc"),
		debug = False,
	)


_tests.new (
		identifier = "apex-to-www-redirect",
		requests = chain.with_host ("google.com"),
		responses = chain.redirect_to ("https://www.google.com/"),
	)

_tests.new (
		identifier = "www-get-/",
		requests = chain.with_host ("www.google.com"),
		responses = chain.expect_200 () .has_body (),
	)

_tests.new (
		identifier = "fail",
		requests = chain.with_host ("example.com"),
		responses = chain.expect_200 () .has_body (),
	)


_execution = _tests.execute ()
_execution.dump (sys.stdout)

