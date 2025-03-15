import pyotp
import time


class Authenticator:
    def __init__(self, label, seed, interval=30):
        self.label = label
        self.interval = interval
        self.__seed = seed
        self.__TOPT = pyotp.TOTP(self.__seed, name=label, interval=interval)
        self.seconds_remaining = self.set_remaining_seconds
        self.expiration = self.set_expiration()
        self.__pin = self.get_one_time_pin()
        self.formatted_otp = self.format_otp()

    def __repr__(self):
        for key, value in self.__TOPT.__dict__.items():
            print(f"{key}: {value}")

    def get_one_time_pin(self):
        if self.expiration > time.time():
            self.__pin = self.__TOPT.now()
            self.seconds_remaining = self.set_remaining_seconds()
            self.expiration = self.set_expiration()
            self.formatted_otp = self.format_otp()
            return self.__TOPT.now()

    def format_otp(self):
        return f"{self.__pin} ({self.seconds_remaining})"

    def get_label(self):
        return self.label

    def set_remaining_seconds(self):
        return int(self.interval - time.time() % self.interval)

    def set_expiration(self):
        return time.time() + self.interval - time.time() % self.interval

    def get_labels(self):
        return {
            "label": self.label,
            "pin": self.get_one_time_pin(),
            "seconds_remaining": self.seconds_remaining,
        }


if __name__ == "__main__":
    from datetime import datetime

    auth = Authenticator("My Account", "JBSW")
    print(auth.__repr__())
    print(f"PIN: {auth.get_one_time_pin()}")
    print(f"Remaining Seconds: {auth.seconds_remaining}")
    print(
        f"Expiration: {datetime.fromtimestamp(auth.expiration).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"Formatted OTP: {auth.formatted_otp}")
    help(datetime)
