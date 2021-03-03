class Teams:

    def __init__(self, team_name):
        if not team_name or team_name is None:
            raise RuntimeError('Invalid team name')
        self.team_name = team_name

    @property
    def team_id(self):
        return self.team_id

    @team_id.setter
    def team_id(self, team_id):
        self.team_id = team_id

    @property
    def team_name(self):
        return self.team_name

    @team_name.setter
    def team_name(self, team_name):
        if not team_name or team_name is None:
            raise RuntimeError('Invalid team name')
        self.team_name = team_name

    @property
    def citid(self):
        return self.citid

    @citid.setter
    def citid(self, citid):
        if not citid or citid is None:
            raise RuntimeError('Invalid ci team id')
        self.citid = citid

