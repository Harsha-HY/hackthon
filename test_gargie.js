const fs = require('fs');
let html = fs.readFileSync('officer.html', 'utf8').replace(/\r\n/g, '\n');

const idx1 = html.indexOf('const DEFAULT_DEPARTMENTS');
const idx2 = html.lastIndexOf('</script>');
let code = html.substring(idx1, idx2);

const elements = {};
function getEl(id) {
  if (!elements[id]) {
    elements[id] = {
      id,
      innerText: '',
      innerHTML: '',
      value: '',
      classList: { add: ()=>{}, remove: ()=>{} },
      appendChild: (child) => {
        if (!elements[id].children) elements[id].children = [];
        elements[id].children.push(child);
      }
    };
  }
  return elements[id];
}

const userGargie = {
  name: 'gargie',
  email: 'gram@gmail.com',
  role: 'officer',
  authority: 'Gram Panchayat (Bogadi Rural)',
  department: 'gp'
};

const sandbox = {
  window: { location: { search: '' }, addEventListener: ()=>{} },
  URLSearchParams: URLSearchParams,
  localStorage: {
    getItem: (k) => {
      if (k === 'current_user') return JSON.stringify(userGargie);
      return null;
    },
    setItem: () => {}
  },
  sessionStorage: {
    getItem: (k) => null,
    setItem: () => {}
  },
  document: {
    getElementById: getEl,
    querySelectorAll: () => []
  },
  setInterval: () => {},
  fetch: async () => ({ ok: false }),
  console: console
};

const testCode = `
try {
  initOfficerSession();
  console.log('initOfficerSession passed! currentAuthorityKey:', currentAuthorityKey);
} catch(e) { console.error('initOfficerSession ERROR:', e); }

try {
  renderCurrentAuthorityUI();
  console.log('renderCurrentAuthorityUI passed!');
} catch(e) { console.error('renderCurrentAuthorityUI ERROR:', e); }

try {
  renderWardsTable();
  console.log('renderWardsTable passed!');
} catch(e) { console.error('renderWardsTable ERROR:', e); }

try {
  renderAreasTable();
  console.log('renderAreasTable passed!');
} catch(e) { console.error('renderAreasTable ERROR:', e); }

try {
  renderPinCodesTable();
  console.log('renderPinCodesTable passed!');
} catch(e) { console.error('renderPinCodesTable ERROR:', e); }

try {
  renderCitizensTable();
  console.log('renderCitizensTable passed! HTML length:', document.getElementById('table-citizens').innerHTML.length);
} catch(e) { console.error('renderCitizensTable ERROR:', e); }

try {
  renderPropertiesTable();
  console.log('renderPropertiesTable passed! HTML length:', document.getElementById('table-properties').innerHTML.length);
} catch(e) { console.error('renderPropertiesTable ERROR:', e); }

try {
  renderApplicationsTable();
  console.log('renderApplicationsTable passed! HTML length:', document.getElementById('table-applications').innerHTML.length);
} catch(e) { console.error('renderApplicationsTable ERROR:', e); }

try {
  renderInspectorsTable();
  console.log('renderInspectorsTable passed! HTML length:', document.getElementById('table-inspectors').innerHTML.length);
} catch(e) { console.error('renderInspectorsTable ERROR:', e); }

try {
  renderDemolitionRequestsTable();
  console.log('renderDemolitionRequestsTable passed! HTML length:', document.getElementById('table-demolition_requests').innerHTML.length);
} catch(e) { console.error('renderDemolitionRequestsTable ERROR:', e); }

try {
  renderCertificatesTable();
  console.log('renderCertificatesTable passed! HTML length:', document.getElementById('table-certificates').innerHTML.length);
} catch(e) { console.error('renderCertificatesTable ERROR:', e); }
`;

const vm = require('vm');
vm.createContext(sandbox);
vm.runInContext(code + testCode, sandbox);
