Module = function () {
    
    var modules = {};

    var mod = function(name) {
        
        if (modules[name])
        {
            return modules[name];
        }
        
        return modules[name] = { moduleName: name };
    };

    return mod;
}();
