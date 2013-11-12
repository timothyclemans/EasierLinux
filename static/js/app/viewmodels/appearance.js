function AppearanceViewModel(settingsViewModel) {
    var self = this;

    self.name = settingsViewModel.appearance_name;
    self.color = settingsViewModel.appearance_color;

    self.brand = ko.computed(function() {
        if (self.name())
            return "OctoFarm: " + self.name();
        else
            return "OctoFarm";
    })

    self.title = ko.computed(function() {
        if (self.name())
            return self.name() + " [OctoFarm]";
        else
            return "OctoFarm";
    })
}
