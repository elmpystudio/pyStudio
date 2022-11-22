'''
This module contains sciluigi's subclasses of luigi's Task class.
'''

import datetime
import luigi
import logging
import os
import sciluigi
import sciluigi.audit
import sciluigi.interface
import sciluigi.dependencies
import sciluigi.slurm
import signal

log = logging.getLogger('sciluigi-interface')

# ==============================================================================

class ElmWorkflowTask(sciluigi.audit.AuditTrailHelpers, luigi.Task):
    '''
    SciLuigi-specific task, that has a method for implementing a (dynamic) workflow
    definition (workflow()).
    '''

    def __init__(self):
        super(ElmWorkflowTask, self).__init__()

        self.instance_name = luigi.Parameter(default='sciluigi_workflow')

        self.tasks = {}
        self.wfstart = ''
        self.wflogpath = ''
        self.hasloggedstart = False
        self.hasloggedfinish = False
        self.hasaddedhandler = False
        self.last_workflow_return = None

    def _ensure_timestamp(self):
        '''
        Make sure that there is a time stamp for when the workflow started.
        '''
        if self.wfstart == '':
            self.wfstart = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')

    def get_wflogpath(self):
        '''
        Get the path to the workflow-speicfic log file.
        '''
        if self.wflogpath == '':
            self._ensure_timestamp()
            clsname = self.__class__.__name__.lower()
            logpath = 'log/workflow_' + clsname + '_started_{t}.log'.format(t=self.wfstart)
            self._wflogpath = logpath
        return self._wflogpath

    def get_auditdirpath(self):
        '''
        Get the path to the workflow-speicfic audit trail directory.
        '''
        self._ensure_timestamp()
        clsname = self.__class__.__name__.lower()
        audit_dirpath = 'audit/.audit_%s_%s' % (clsname, self.wfstart)
        return audit_dirpath

    def get_auditlogpath(self):
        '''
        Get the path to the workflow-speicfic audit trail file.
        '''
        self._ensure_timestamp()
        clsname = self.__class__.__name__.lower()
        audit_dirpath = 'audit/workflow_%s_started_%s.audit' % (clsname, self.wfstart)
        return audit_dirpath

    def add_auditinfo(self, infotype, infolog):
        '''
        Add audit information to the audit log.
        '''
        return self._add_auditinfo(self.__class__.__name__.lower(), infotype, infolog)

    def set_workflow_return(self, return_tasks):
        self.last_workflow_return = return_tasks

    def workflow(self):
        '''
        SciLuigi API methoed. Implement your workflow here, and return the last task(s)
        of the dependency graph.
        '''
        if self.last_workflow_return is None:
            raise WorkflowNotImplementedException(
                    'workflow() method is not implemented, for ' + str(self))
        else:
            return self.last_workflow_return

    def requires(self):
        '''
        Implementation of Luigi API method.
        '''
        if not self.hasaddedhandler:
            wflog_formatter = logging.Formatter(
                    sciluigi.interface.LOGFMT_STREAM,
                    sciluigi.interface.DATEFMT)
            wflog_file_handler = logging.FileHandler(self.output()['log'].path)
            wflog_file_handler.setLevel(logging.INFO)
            wflog_file_handler.setFormatter(wflog_formatter)
            log.addHandler(wflog_file_handler)
            luigilog = logging.getLogger('luigi-interface')
            luigilog.addHandler(wflog_file_handler)
            self.hasaddedhandler = True
        clsname = self.__class__.__name__
        if not self.hasloggedstart:
            log.info('-'*80)
            log.info('SciLuigi: %s Workflow Started (logging to %s)', clsname, self.get_wflogpath())
            log.info('-'*80)
            self.hasloggedstart = True
        workflow_output = self.workflow()
        if workflow_output is None:
            clsname = self.__class__.__name__
            raise Exception(('Nothing returned from workflow() method in the %s Workflow task. '
                             'Forgot to add a return statement at the end?') % clsname)
        return workflow_output

    def output(self):
        '''
        Implementation of Luigi API method
        '''
        return {'log': luigi.LocalTarget(self.get_wflogpath()),
                'audit': luigi.LocalTarget(self.get_auditlogpath())}

    def run(self):
        '''
        Implementation of Luigi API method
        '''
        if self.output()['audit'].exists():
            errmsg = ('Audit file already exists, '
                      'when trying to create it: %s') % self.output()['audit'].path
            log.error(errmsg)
            raise Exception(errmsg)
        else:
            with self.output()['audit'].open('w') as auditfile:
                for taskname in sorted(self.tasks):
                    taskaudit_path = os.path.join(self.get_auditdirpath(), taskname)
                    if os.path.exists(taskaudit_path):
                        auditfile.write(open(taskaudit_path).read() + '\n')
        clsname = self.__class__.__name__
        if not self.hasloggedfinish:
            log.info('-'*80)
            log.info('SciLuigi: %s Workflow Finished (workflow log at %s)', clsname, self.get_wflogpath())
            log.info('-'*80)
            self.hasloggedfinish = True

    def new_task(self, instance_name, cls, **kwargs):
        '''
        Create new task instance, and link it to the current workflow.
        '''
        newtask = sciluigi.new_task(instance_name, cls, self, **kwargs)
        self.tasks[instance_name] = newtask
        return newtask

# ================================================================================

class WorkflowNotImplementedException(Exception):
    '''
    Exception to throw if the workflow() SciLuigi API method is not implemented.
    '''
    pass
