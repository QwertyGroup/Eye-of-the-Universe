import gspread
import uuid
import Core.CloudGuard as CloudG

cred = CloudG.GetGooCred()
cl = gspread.authorize(cred)


class Item:
    def __init__(self, name, type, GUID):
        self.name = name
        self.type = type
        self.GUID = GUID


class BasicL:
    def __init__(self, ssh):
        self.ssh = ssh
        self.user = None
        BasicL.local = ssh.worksheet('Local')
        BasicL.BoxBox = ssh.worksheet('Box-Box')
        BasicL.BoxWave = ssh.worksheet('Box-Wave')

    def GetBoxChildren(self, boxGUID):
        if boxGUID == None or boxGUID == '': 
            boxGUID = self.user.GUID 
            self.user.WriteField('CurrentBox', boxGUID)

        # TODO: connect to db and get all boxes and waves from user.regRow
        # then execCmds: handle new FileView by GUID
        # new files: GUID = uuid.uuid4() - that is random uuid/guid
    
        #test = [Item('item1','box','id1'),
        #        Item('item2','box','id2'),
        #        Item('item3','box','id3'),
        #        Item('item4','box','id4'),
        #        Item('item5','box','id5'),
        #        Item('item6','wave','id6'),
        #        Item('item7','wave','id7')]
        #return test
        
        # For Boxes:
        nextEmpty = self.ParentNext(boxGUID)
        childrenSigns = list()
        if nextEmpty.col > 2: 
            childrenSigns = self.BoxBox.range(nextEmpty.row, 2, nextEmpty.row, nextEmpty.col - 1)
            childrenSigns = [cell.value for cell in childrenSigns if cell.value != 'removed']
        children = list()
        for sign in childrenSigns:
            chGUID, chName = sign.split(':') # we cant use ":" in box name!
            children.append(Item(chName, 'box', chGUID))

        return children

    def CreateBox(self, name='New Box'):
        parent = self.user.ReadField('CurrentBox')
        if not self.BoxExist(parent):
            lastEmpty = self.GetLastEmptyBoxAndIter()
            self.BoxBox.update_cell(lastEmpty, 1, parent)
        childGUID = self.CreateChildBox(parent, name)
    
    def ReadLocal(self, key):
        keyCell = self.local.find(key)
        valueCell = self.local.cell(keyCell.row, keyCell.col + 1)
        return valueCell.value

    def WriteLocal(self, key, val):
        keyCell = self.local.find(key)
        self.local.update_cell(keyCell.row, keyCell.col + 1, val)

    def BoxExist(self, boxGUID):
        matches = self.BoxBox.findall(boxGUID)
        for cell in matches:
            if cell.col == 1:
                return True
        return False

    def GetLastEmptyBoxAndIter(self):
        lastEmpty = self.ReadLocal('LastBoxEmpty')
        self.WriteLocal('LastBoxEmpty', str(int(lastEmpty) + 1))
        return lastEmpty

    def CreateChildBox(self, parentGUID, childName):
        # create new box
        # and add to parent children
        childGUID = uuid.uuid4()
        lastEmpty = self.GetLastEmptyBoxAndIter()
        self.BoxBox.update_cell(lastEmpty, 1, childGUID)
        emptyCell = self.ParentNext(parentGUID)
        self.BoxBox.update_cell(emptyCell.row, emptyCell.col, f'{childGUID}:{childName}') # TODO: create new sheet with GUID: name Dict
        
    def ParentNext(self, parentGUID):
        parentCell = self.BoxCell(parentGUID)
        counter = 1
        shift = 10
        while True:
            rng = self.BoxBox.range(parentCell.row, counter, parentCell.row, counter + shift)
            for cell in rng:
                if cell.value == None or cell.value == '':
                    return cell
            counter += shift

    def BoxCell(self, boxGUID):
         matches = self.BoxBox.findall(boxGUID)
         for cell in matches:
             if cell.col == 1:
                 return cell
         return None

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
        rng = [cell.value for cell in self.register.range(f'A1:{self.LastEmptyCell()}') if cell.value != 'removed']
        if len(rng) == 1:
            return list()
        else:
            rng.pop()
            return rng

    def Remove(self, row):
        self.register.update_cell(row, 1, 'removed')

    def Add(self, GUID):
        self.register.update_acell(self.LastEmptyCell(), GUID)
        row = self.LastEmptyRow()
        self.IncrimentLastEmpty()
        return row

    def Exist(self, GUID):
        return GUID in self.Community()

    fieldDict = {'GUID': 1, 'Row': 2, 'CurrentBox': 3}  # key:col

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
