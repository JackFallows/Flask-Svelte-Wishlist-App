import Jasmine from 'jasmine';
import jasmineReporters from 'jasmine-reporters';

async function jasmineTests() {
    var jasmine = new Jasmine();

    jasmine.loadConfigFile('./spec/support/jasmine.json');
    
    var junitReporter = new jasmineReporters.JUnitXmlReporter({
        savePath: './test-results',
        consolidateAll: false
    });
    jasmine.addReporter(junitReporter);

    await jasmine.execute();
}

jasmineTests();
