import gspread
import Core.CloudGuard as CloudG

cred = CloudG.GetGooCred()
cl = gspread.authorize(cred)


class BasicL:
    def __init__(self, ssh):
        self.ssh = ssh


class SteelMountainL(BasicL):
    def __init__(self):
        ssh = cl.open_by_key('1yYsBTlfNESP2U5SHQ8OI5nRPxfFkmtdHH9wSdgzrkzg')
        BasicL.__init__(self, ssh)
        BasicL.Name = "SteelMountainL"


class DigitalExpanseL(BasicL):
    def __init__(self):
        ssh = cl.open_by_key('1UwDzbUgMAnJdG05OPUo9J-lrYkkFT_Uu8QXnqiE4NsM')
        BasicL.__init__(self, ssh)
        BasicL.Name = "DigitalExpanseL"


class Register():
    def __init__(self):
        self.ssh = cl.open_by_key('1Mx1ZsnxulQUHzAg0Do8CV0MexmWzZINQm-GcOAPj94M')
        self.register = self. ssh.worksheet('Register')
        self.local = self.ssh.worksheet('Local')

    def LastEmptyCell(self):
        return self.ReadLocalValue('Last empty cell')

    def LastEmptyRow(self):
        return int(self.ReadLocalValue('Last empty row'))

    def IncrimentLastEmpty(self):
        val = self.LastEmptyRow()
        self.UpdateLocalValue('Last empty row', val + 1)
        self.UpdateLocalValue('Last empty cell', f'A{val+1}')

    def ReadLocalValue(self, key):
        keyCell = self.local.find(key)
        valueCell = self.local.cell(keyCell.row, keyCell.col + 1)
        return valueCell.value

    def UpdateLocalValue(self, key, val):
        keyCell = self.local.find(key)
        self.local.update_cell(keyCell.row, keyCell.col + 1, val)

    def Community(self):
        rng = [cell.value for cell in self.register.range(f'A1:{self.LastEmptyCell()}')]
        if len(rng) == 1:
            return list()
        else:
            rng.pop()
            return rng

    def Remove(self, row):
        print('here')
        self.register.update_cell(row, 1, 'removed')

    def Add(self, GUID):
        self.register.update_acell(self.LastEmptyCell(), GUID)
        row = self.LastEmptyRow()
        self.IncrimentLastEmpty()
        return row

    def Exist(self, GUID):
        return GUID in self.Community()

    fieldDict = {'GUID': 1, 'Row': 2}  # key:col

    def ReadField(self, individual, key):
        row = self.IndividualRow(individual)
        return self.register.cell(row, self.fieldDict[key]).value

    def WriteField(self, individual, key, val):
        row = self.IndividualRow(individual)
        self.register.update_cell(row, self.fieldDict[key], val)

    def IndividualRow(self, individual):
        if individual.regRow == None:
            row = self.register.find(individual.GUID).row
            self.register.update_cell(row, self.fieldDict['Row'], row)
            return row
        else:
            return individual.regRow
