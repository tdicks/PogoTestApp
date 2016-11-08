from enum import Enum
from ATE.adc import Channel
from ATE.gui import MainForm

class TestSuite(object):
    "Suite of tests for the user to complete. Controls the running and state of tests. Call TestSuite.reset() before interacting with any tests. "
    tests = []
    current_test = -1
    form = None

    def execute(self):
        self.tests[self.current_test].breakout = False
        self.form.update_current_test(self.tests[self.current_test])
        self.tests[self.current_test].setUp()
        self.tests[self.current_test].run()
        self.tests[self.current_test].tearDown()

    def add_test(self, test):
        test.suite = self
        self.tests.append(test)

    def set_text(self, text):
        self.form.info_label["text"] = text

    def append_text(self, text):
        self.form.info_label["text"] += "\n" + text

    def pass_test(self):
        self.tests[self.current_test].set_passed()
        self.advance_test()

    def fail_test(self):
        self.tests[self.current_test].set_failed()
        if self.tests[self.current_test].aborts:
            self.summary()
        else:
            self.advance_test()

    def reset(self):
        # If we've just loaded up, go ahead and start from the beginning
        if self.current_test == -1:
            self.current_test = 0
            self.execute()
            return

        answer = self.form.resetdialogue()
        if answer == True:
            self.execute()
        elif answer == False:
            self.reset_test_results()
            self.current_test = 0
            self.execute()

    def reset_test_results(self):
        for test in self.tests:
            test.reset()

    def advance_test(self):

        # Check to see if we've got more groups to run. If we don't, show the summary.
        if self.current_test >= len(self.tests) -1:
            # If our form is declared, run the summary method. If not, we're likely running from unit tests so ignore.
            if self.form:
                self.summary()
        else:
            # If we do have more tests, advance the current test variable and execute the test.
            self.current_test += 1
            self.execute()

    def summary(self):
        self.current_test = -1

        results = "Test suite completed. Results:\n\n"
        tests = len(self.tests)
        failures = 0
        passes = 0

        for test in self.tests:
            results += "{0}: {1}\n".format(test.__doc__, test.format_state())
            if test.state == "failed":
                failures += 1
            if test.state == "passed":
                passes += 1

        results += "\n\nTests: {}, Passes: {}, Failures: {}".format(tests, passes, failures)

        if failures > 0:
            self.form.info_label["bg"] = "darkred"
        elif failures == 0 and passes > 0:
            self.form.info_label["bg"] = "darkgreen"

        self.set_text(results)
        self.form.disable_test_buttons()
