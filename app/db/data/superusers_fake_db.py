"""This file is meant to mock a user database and is commited to git history
just for the convenience of the developer reading this code: personal data
should never be published in repositories.
"""
superusers_db = {
    'guane': {
        "username": "guane",
        "full_name": "guane enterprises",
        # password: ilovethori
        "hashed_password": "$2b$12$ESVIIGyxIcIPaYsZuSKIFOmqwTMbtePT6GnoKf0ufwDjoietMVauO",  # noqa
        "disabled": False
    },
    'juanes': {
        "username": "juanes",
        "full_name": "Juan Esteban",
        # password: ilovecharliebot
        "hashed_password": "$2b$12$Mky.p4UlRtZAc.1IKQayHO8zJuMf.NoblVAT0xehuj6oANUBbsqZ.",  # noqa
        "disabled": False
    }
}
