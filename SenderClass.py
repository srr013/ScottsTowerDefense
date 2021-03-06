import operator

import Enemy
import Localdefs
import Player


class Sender():
    '''called from EventFunctions. Creates a sender that creates the enemies.'''

    def __init__(self, **kwargs):
        self.specialSend = kwargs['specialSend']
        if self.specialSend:
            self.enemytype = 'Crowd'
            self.pos = kwargs['pos']
            self.wave = kwargs['curwave']
            self.numThisWave = kwargs['number']
            self.enemycounter = self.enemycounterinit = kwargs['deploySpeed']
        else:
            self.wave = Player.player.wavenum
            self.enemytype = Player.player.waveList[self.wave]['enemytype']
            self.numThisWave = Player.player.waveList[self.wave]['enemynum']
            self.enemycounter = self.enemycounterinit = eval("Enemy." + self.enemytype + ".deploySpeed")
        self.enemiesDeployed = 0
        self.isBoss = Player.player.waveList[self.wave]['isboss']
        Localdefs.senderlist.append(self)
        #print (self.enemytype), Player.player.waveList[Player.player.wavenum]

    def tick(self):
        '''Sends enemies and maintains Senderlist'''
        self.enemycounter -= Player.player.frametime
        if self.enemycounter <= 0 or self.enemiesDeployed == 0:
            Player.player.analytics.gameEnemies +=1
            if self.enemiesDeployed < self.numThisWave:
                if self.enemytype == 'Crowd' and self.specialSend == True:

                    f = operator.methodcaller(self.enemytype, isBoss=self.isBoss, specialSend=self.specialSend,
                                              pos=self.pos, wave = self.wave, enemyNum = self.enemiesDeployed)
                    f(Enemy)
                else:
                    f = operator.methodcaller(self.enemytype, isBoss=self.isBoss, specialSend=self.specialSend, wave = self.wave,
                                              enemyNum = self.enemiesDeployed)
                    f(Enemy)
                self.enemiesDeployed += 1
            else:
                Localdefs.senderlist.remove(self)

            self.enemycounter = self.enemycounterinit
