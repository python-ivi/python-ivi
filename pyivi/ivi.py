"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import inspect

# try importing drivers
try:
    import vxi11
except:
    pass

try:
    from . import linuxgpib
except:
    pass

from functools import partial

class X(object):
    def __init__(self,_d={},**kwargs):
        kwargs.update(_d)
        self.__dict__=kwargs


# Exceptions

class IviException(Exception): pass
class IviDriverException(IviException): pass
class FileFormatException(IviDriverException): pass
class IdQueryFailedException(IviDriverException): pass
class InstrumentStatusExcpetion(IviDriverException): pass
class InvalidOptionValueException(IviDriverException): pass
class IOException(IviDriverException): pass
class IOTimeoutException(IviDriverException): pass
class MaxTimeoutExceededException(IviDriverException): pass
class NotInitializedException(IviDriverException): pass
class OperationNotSupportedException(IviDriverException): pass
class OperationPendingException(IviDriverException): pass
class OptionMissingException(IviDriverException): pass
class OptionStringFormatException(IviDriverException): pass
class OutOfRangeException(IviDriverException): pass
class ResetFailedException(IviDriverException): pass
class ResetNotSupportedException(IviDriverException): pass
class SelectorFormatException(IviDriverException): pass
class SelectorHierarchyException(IviDriverException): pass
class SelectorNameException(IviDriverException): pass
class SelectorNameRequiredException(IviDriverException): pass
class SelectorRangeException(IviDriverException): pass
class SimulationStateException(IviDriverException): pass
class TriggerNotSoftwareException(IviDriverException): pass
class UnexpectedResponseException(IviDriverException): pass
class UnknownOptionException(IviDriverException): pass
class UnknownPhysicalNameException(IviDriverException): pass
class ValueNotSupportedException(IviDriverException): pass


def get_index(l, i):
    if i in l:
        return l.index(i)
    if type(i) == int:
        if i < 0 or i >= len(l):
            raise SelectorRangeException()
        return i
    raise SelectorNameException()


class PropertyCollection(object):
    def __init__(self):
        object.__setattr__(self, '_props', dict())
        object.__setattr__(self, '_locked', False)
    
    def _add_property(self, name, fget=None, fset=None, fdel=None):
        object.__getattribute__(self, '_props')[name] = (fget, fset, fdel)
        object.__setattr__(self, name, None)
    
    def _add_method(self, name, f=None):
        object.__setattr__(self, name, f)
    
    def _del_property(self, name):
        del object.__getattribute__(self, '_props')[name]
        del object.__dict__[name]
    
    def _lock(self, lock=True):
        object.__setattr__(self, '_locked', lock)
        
    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '_props'):
            f = object.__getattribute__(self, '_props')[name][0]
            if f is None:
                raise AttributeError("unreadable attribute")
            return f()
        return object.__getattribute__(self, name)
        
    def __setattr__(self, name, value):
        if name in object.__getattribute__(self, '_props'):
            f = object.__getattribute__(self, '_props')[name][1]
            if f is None:
                raise AttributeError("can't set attribute")
            f(value)
            return
        if name not in object.__dict__ and self._locked:
            raise AttributeError("locked")
        object.__setattr__(self, name, value)
        
    def __delattr__(self, name):
        if name in object.__getattribute__(self, '_props'):
            f = object.__getattribute__(self, '_props')[name][2]
            if f is None:
                raise AttributeError("can't delete attribute")
            f()
            return
        del object.__dict__[name]
        

class IndexedPropertyCollection(object):
    def __init__(self):
        self._props = dict()
        self._indicies = list()
        self._objs = list()
    
    def _add_property(self, name, fget=None, fset=None, fdel=None):
        self._props[name] = (fget, fset, fdel)
    
    def _add_method(self, name, f=None):
        self._props[name] = f
    
    def _add_sub_property(self, sub, name, fget=None, fset=None, fdel=None):
        if sub not in self._props:
            self._props[sub] = dict()
        if type(self._props[sub]) != dict:
            raise AttributeError("property %s already defined" % sub)
        self._props[sub][name] = (fget, fset, fdel)
    
    def _add_sub_method(self, sub, name, f=None):
        if sub not in self._props:
            self._props[sub] = dict()
        if type(self._props[sub]) != dict:
            raise AttributeError("property %s already defined" % sub)
        self._props[sub][name] = f
    
    def _del_property(self, name):
        del self._props[name]
    
    def _build_obj(self, d, i):
        obj = PropertyCollection()
        for n in d:
            itm = d[n]
            if type(itm) == tuple:
                fget, fset, fdel = itm
                fgeti = fseti = fdeli = None
                if fget is not None: fgeti = partial(fget, i)
                if fset is not None: fseti = partial(fset, i)
                if fdel is not None: fdeli = partial(fdel, i)
                obj._add_property(n, fgeti, fseti, fdeli)
            elif type(itm) == dict:
                o2 = self._build_obj(itm, i)
                obj.__dict__[n] = o2
            elif hasattr(itm, "__call__"):
                obj.__dict__[n] = partial(itm, i)
        return obj
    
    def _set_list(self, l):
        self._indicies = list(l)
        self._objs = list()
        for i in range(len(self._indicies)):
            self._objs.append(self._build_obj(self._props, i))
    
    def __getitem__(self, key):
        i = get_index(self._indicies, key)
        return self._objs[i]
    
    def __len__(self):
        return len(self._indicies)
        
    def count(self):
        return len(self._indicies)


class DriverOperation(object):
    "Inherent IVI methods for driver operation"
    
    def __init__(self):
        super(DriverOperation, self).__init__()
        
        self._driver_operation_cache = True
        self._driver_operation_driver_setup = ""
        self._driver_operation_interchange_check = False
        self._driver_operation_logical_name = ""
        self._driver_operation_query_instrument_status = False
        self._driver_operation_range_check = True
        self._driver_operation_record_coercions = False
        self._driver_operation_io_resource_descriptor = ""
        self._driver_operation_simulate = False
        
        self._driver_operation_interchange_warnings = list()
        self._driver_operation_coercion_records = list()
        
        self.__dict__.setdefault('driver_operation', PropertyCollection())
        self.driver_operation._add_property('cache',
                        self._get_driver_operation_cache,
                        self._set_driver_operation_cache)
        self.driver_operation._add_property('driver_setup',
                        self._get_driver_operation_driver_setup)
        self.driver_operation._add_property('interchange_check',
                        self._get_driver_operation_interchange_check,
                        self._set_driver_operation_interchange_check)
        self.driver_operation._add_property('logical_name',
                        self._get_driver_operation_logical_name)
        self.driver_operation._add_property('query_instrument_status',
                        self._get_driver_operation_query_instrument_status,
                        self._set_driver_operation_query_instrument_status)
        self.driver_operation._add_property('range_check',
                        self._get_driver_operation_range_check,
                        self._set_driver_operation_range_check)
        self.driver_operation._add_property('record_coercions',
                        self._get_driver_operation_record_coercions,
                        self._set_driver_operation_record_coercions)
        self.driver_operation._add_property('io_resource_descriptor',
                        self._get_driver_operation_io_resource_descriptor)
        self.driver_operation._add_property('simulate',
                        self._get_driver_operation_simulate,
                        self._set_driver_operation_simulate)
        self.driver_operation._add_property('simulate',
                        self._get_driver_operation_simulate)
        self.driver_operation.clear_interchange_warnings = self._driver_operation_clear_interchange_warnings
        self.driver_operation.get_next_coercion_record = self._driver_operation_get_next_coercion_record
        self.driver_operation.get_next_interchange_warning = self._driver_operation_get_next_interchange_warning
        self.driver_operation.invalidate_all_attributes = self._driver_operation_invalidate_all_attributes
        self.driver_operation.reset_interchange_check = self._driver_operation_reset_interchange_check
    
    
    def _get_driver_operation_cache(self):
        return self._driver_operation_cache
    
    def _set_driver_operation_cache(self, value):
        self._driver_operation_cache = bool(value)
    
    def _get_driver_operation_driver_setup(self):
        return self._driver_operation_driver_setup
    
    def _get_driver_operation_interchange_check(self):
        return self._driver_operation_interchange_check
    
    def _set_driver_operation_interchange_check(self, value):
        self._driver_operation_interchange_check = bool(value)
    
    def _get_driver_operation_logical_name(self):
        return self._driver_operation_logical_name
    
    def _get_driver_operation_query_instrument_status(self):
        return self._driver_operation_query_instrument_status
    
    def _set_driver_operation_query_instrument_status(self, value):
        self._driver_operation_query_instrument_status = bool(value)
    
    def _get_driver_operation_range_check(self):
        return self._driver_operation_range_check
    
    def _set_driver_operation_range_check(self, value):
        self._driver_operation_range_check = bool(value)
    
    def _get_driver_operation_record_coercions(self):
        return self._driver_operation_record_coercions
    
    def _set_driver_operation_record_coercions(self, value):
        self._driver_operation_record_coercions = bool(value)
    
    def _get_driver_operation_io_resource_descriptor(self):
        return self._driver_operation_io_resource_descriptor
    
    def _get_driver_operation_simulate(self):
        return self._driver_operation_simulate
    
    def _set_driver_operation_simulate(self, value):
        value = bool(value)
        if self._driver_operation_simulate and not value:
            raise SimulationStateException()
        self._driver_operation_simulate = value
    
    def _driver_operation_clear_interchange_warnings(self):
        self._driver_operation_interchange_warnings = list()
    
    def _driver_operation_get_next_coercion_record(self):
        if len(self._driver_operation_coercion_records) > 0:
            return self._driver_operation_coercion_records.pop()
        return ""
    
    def _driver_operation_get_next_interchange_warning(self):
        if len(self._driver_operation_interchange_warnings) > 0:
            return self._driver_operation_interchange_warnings.pop()
        return ""
    
    def _driver_operation_invalidate_all_attributes(self):
        pass
    
    def _driver_operation_reset_interchange_check(self):
        pass
    
    

class DriverIdentity(object):
    "Inherent IVI methods for identification"
    
    def __init__(self):
        super(DriverIdentity, self).__init__()
        
        self._identity_description = "Base IVI Driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = ""
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list()
        self.__dict__.setdefault('_identity_group_capabilities', list())
        
        self.__dict__.setdefault('identity', PropertyCollection())
        self.identity._add_property('description',
                        self._get_identity_description)
        self.identity._add_property('identifier',
                        self._get_identity_identifier)
        self.identity._add_property('revision',
                        self._get_identity_revision)
        self.identity._add_property('vendor',
                        self._get_identity_vendor)
        self.identity._add_property('instrument_manufacturer',
                        self._get_identity_instrument_manufacturer)
        self.identity._add_property('instrument_model',
                        self._get_identity_instrument_model)
        self.identity._add_property('instrument_firmware_revision',
                        self._get_identity_instrument_firmware_revision)
        self.identity._add_property('specification_major_version',
                        self._get_identity_specification_major_version)
        self.identity._add_property('specification_minor_version',
                        self._get_identity_specification_minor_version)
        self.identity._add_property('supported_instrument_models',
                        self._get_identity_supported_instrument_models)
        self.identity._add_property('group_capabilities',
                        self._get_identity_group_capabilities)
        self.identity.get_group_capabilities = self._identity_get_group_capabilities
        self.identity.get_supported_instrument_models = self._identity_get_supported_instrument_models
    
    
    def _get_identity_description(self):
        return self._identity_description
    
    def _get_identity_identifier(self):
        return self._identity_identifier
    
    def _get_identity_revision(self):
        return self._identity_revision
    
    def _get_identity_vendor(self):
        return self._identity_vendor
    
    def _get_identity_instrument_manufacturer(self):
        return self._identity_instrument_manufacturer
    
    def _get_identity_instrument_model(self):
        return self._identity_instrument_model
    
    def _get_identity_instrument_firmware_revision(self):
        return self._identity_instrument_firmware_revision
    
    def _get_identity_specification_major_version(self):
        return self._identity_specification_major_version
    
    def _get_identity_specification_minor_version(self):
        return self._identity_specification_minor_version
    
    def _get_identity_supported_instrument_models(self):
        return ",".join(self._identity_supported_instrument_models)
    
    def _get_identity_group_capabilities(self):
        return ",".join(self._identity_group_capabilities)
    
    def _identity_get_group_capabilities(self):
        return self._identity_group_capabilities
    
    def _identity_get_supported_instrument_models(self):
        return self._identity_supported_instrument_models
    
    

class DriverUtility(object):
    "Inherent IVI utility methods"
    
    def __init__(self):
        super(DriverUtility, self).__init__()
        
        self.__dict__.setdefault('utility', PropertyCollection())
        self.utility.disable = self._utility_disable
        self.utility.error_query = self._utility_error_query
        self.utility.lock_object = self._utility_lock_object
        self.utility.reset = self._utility_reset
        self.utility.reset_with_defaults = self._utility_reset_with_defaults
        self.utility.self_test = self._utility_self_test
        self.utility.unlock_object = self._utility_unlock_object
    
    
    def _utility_disable(self):
        pass
    
    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        return (error_code, error_message)
    
    def _utility_lock_object(self):
        pass
    
    def _utility_reset(self):
        pass
    
    def _utility_reset_with_defaults(self):
        self.utility_reset()
    
    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        return (code, message)
    
    def _utility_unlock_object(self):
        pass
    
    

class Driver(DriverOperation, DriverIdentity, DriverUtility):
    "Inherent IVI methods for all instruments"
    
    def __init__(self):
        super(Driver, self).__init__()
        self._interface = None
        self._initialized = False
        self._instrument_id = ''
        self._cache_valid = list()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        # decode options
        for op in keywargs:
            val = keywargs[op]
            if op == 'range_check':
                self._driver_operation_range_check = bool(val)
            elif op == 'query_instr_status':
                self._driver_operation_query_instrument_status = bool(val)
            elif op == 'cache':
                self._driver_operation_cache = bool(val)
            elif op == 'simulate':
                self._driver_operation_simulate = bool(val)
            elif op == 'record_coercions':
                self._driver_operation_record_coercions = bool(val)
            elif op == 'interchange_check':
                self._driver_operation_interchange_check = bool(val)
            elif op == 'driver_setup':
                self._driver_operation_driver_setup = val
            else:
                raise UnknownOptionException('Invalid option')
        
        # process resource
        if self._driver_operation_simulate:
            print("Simulating; ignoring resource")
        elif resource is None:
            raise IOException('No resource specified!')
        elif type(resource) == str:
            # parse VISA resource string
            # valid resource strings:
            # TCPIP::10.0.0.1::INSTR
            # TCPIP0::10.0.0.1::INSTR
            # TCPIP::10.0.0.1::gpib,5::INSTR
            # TCPIP0::10.0.0.1::gpib,5::INSTR
            # GPIB::10::INSTR
            # GPIB0::10::INSTR
            res = resource.split("::")
            if len(res) == 1:
                raise IOException('Invalid resource name')
            
            t = res[0].upper()
            
            if t[:5] == 'TCPIP':
                # TCP connection
                host = res[1]
                name = None
                if len(res) == 4:
                    name = res[2]
                
                if 'vxi11' in globals():
                    # connect with VXI-11
                    self._interface = vxi11.Instrument(host, name)
                else:
                    raise IOException('Cannot use resource type %s' % t)
            elif t[:4] == 'GPIB':
                # GPIB connection
                index = t[4:]
                if len(index) > 0:
                    index = int(index)
                else:
                    index = 0
                
                addr = int(res[1])
                
                if 'linuxgpib' in globals():
                    # connect with linux-gpib
                    self._interface = linuxgpib.LinuxGpibInstrument(index, addr)
                else:
                    raise IOException('Cannot use resource type %s' % t)
                
            else:
                raise IOException('Unknown resource type %s' % t)
            
            _driver_operation_io_resource_descriptor = resource
            
        elif 'vxi11' in globals() and type(resource) == vxi11.Instrument:
            # Got a vxi11 instrument, can use it as is
            self._interface = resource
        else:
            # don't have a usable resource
            raise IOException('Invalid resource')
        
        self.driver_operation.invalidate_all_attributes()
        
        self._initialized = True
        
        
    def close(self):
        "Closes an IVI session"
        if self._interface:
            try:
                self._interface.close()
            except:
                pass
        
        self._interface = None
        self._initialized = False
        
        
    def _get_initialized(self):
        "Returnes initialization state of driver"
        return self._initialized
        
    initialized = property(_get_initialized)
    
    def _get_cache_tag(self, tag=None, skip=1):
        if tag is None:
            stack = inspect.stack()
            start = 0 + skip
            if len(stack) < start + 1:
                return ''
            tag = stack[start][3] 
        
        if tag[0:4] == "_get": tag = tag[4:]
        if tag[0:4] == "_set": tag = tag[4:]
        if tag[0] == "_": tag = tag[1:]
        
        return tag
    
    def _get_cache_valid(self, tag=None, index=-1, skip_disable=False):
        if not skip_disable and not self._driver_operation_cache:
            return False
        tag = self._get_cache_tag(tag, 2)
        if index >= 0:
            tag = tag + '_%d' % index
        return tag in self._cache_valid
    
    def _set_cache_valid(self, valid=True, tag=None, index=-1):
        tag = self._get_cache_tag(tag, 2)
        if index >= 0:
            tag = tag + '_%d' % index
        if valid:
            if tag not in self._cache_valid:
                self._cache_valid.append(tag)
        else:
            if tag in self._cache_valid:
                self._cache_valid.remove(tag)
    
    def _driver_operation_invalidate_all_attributes(self):
        self._cache_valid = list()
    
    def _write_raw(self, data):
        "Write binary data to instrument"
        if self._driver_operation_simulate:
            print("[simulating] Call to write_raw")
            return
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        self._interface.write_raw(data)
    
    def _read_raw(self, num=-1):
        "Read binary data from instrument"
        if self._driver_operation_simulate:
            print("[simulating] Call to read_raw")
            return b''
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        return self._interface.read_raw(num)
    
    def _ask_raw(self, data, num=-1):
        "Write then read binary data"
        if self._driver_operation_simulate:
            print("[simulating] Call to ask_raw")
            return b''
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        return self._interface.ask_raw(data, num)
    
    def _write(self, data, encoding = 'utf-8'):
        "Write string to instrument"
        if self._driver_operation_simulate:
            print("[simulating] Write (%s) '%s'" % (encoding, data))
            return
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        self._interface.write(data, encoding)
    
    def _read(self, num=-1, encoding = 'utf-8'):
        "Read string from instrument"
        if self._driver_operation_simulate:
            print("[simulating] Read (%s)" % encoding)
            return ''
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        return self._interface.read(num, encoding)
    
    def _ask(self, data, num=-1, encoding = 'utf-8'):
        "Write then read string"
        if self._driver_operation_simulate:
            print("[simulating] Ask (%s) '%s'" % (encoding, data))
            return ''
        if not self._initialized or self._interface is None:
            raise NotInitializedException()
        return self._interface.ask(data, num, encoding)
    
    
    
