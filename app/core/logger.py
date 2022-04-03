import spdlog as spd


logger = spd.ConsoleLogger("MercuryAPI", colored=True)
logger.set_pattern("%^[%T] %n: %v%$")
logger.set_level(spd.LogLevel.DEBUG)

"""
trace
debug
info
warn
error
critical
"""
