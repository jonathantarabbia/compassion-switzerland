# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Philippe Heer <heerphilippe@msn.com>
#
#    The licence is in the file __openerp__.py
#
##############################################################################
from openerp import models


class ProjectLifecycle(models.Model):
    """ Send Communication when icp lifecycle is received. """
    _inherit = 'compassion.project.ile'

    def process_commkit(self, commkit_data):
        ids = super(ProjectLifecycle, self).process_commkit(commkit_data)

        for lifecycle in self.browse(ids):
            if lifecycle.type == 'Reactivation' or \
                    lifecycle.type == 'Suspension':

                for child in self.env['compassion.child'].\
                        search([('project_id', '=', lifecycle.project_id.id),
                                ('sponsor_id', '!=', False)]):
                    communication_type = self.env.ref(
                        'sponsorship_switzerland.project_lifecycle')
                    self.env['partner.communication.job'].create({
                        'config_id': communication_type.id,
                        'partner_id': child.sponsor_id.id,
                        'object_id': child.id,
                    })
        return ids
