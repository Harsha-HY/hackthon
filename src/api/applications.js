try { require('dotenv').config(); } catch(e) {}
const { supabase, mapAppToDb, mapDbToApp, mapUserToDb, mapDbToUser } = require('../lib/supabase');

function sendJson(res, statusCode, data) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (typeof res.status === 'function' && typeof res.json === 'function') {
    return res.status(statusCode).json(data);
  }
  res.writeHead(statusCode, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    if (typeof res.status === 'function') return res.status(204).end();
    res.writeHead(204);
    res.end();
    return;
  }

  const method = req.method || 'GET';

  if (method === 'GET') {
    let apps = [];
    if (supabase) {
      try {
        const { data: suApps, error } = await supabase.from('applications').select('*').order('created_at', { ascending: false });
        if (!error && Array.isArray(suApps)) {
          apps = suApps.map(mapDbToApp);
        }
      } catch(e) {
        console.warn('Supabase fetchApplications error:', e);
      }
    }

    const query = req.query || {};
    if (query.inspector) {
      const insEmail = query.inspector.toLowerCase().trim();
      apps = apps.filter(a => (a.assignedInspectorEmail || '').toLowerCase() === insEmail || (a.auditedBy || '').toLowerCase() === insEmail);
    }
    if (query.pin) {
      const p = String(query.pin).trim();
      apps = apps.filter(a => String(a.pincode || a.pin || '').trim() === p || String(a.pincode || a.pin || '').startsWith(p));
    }
    if (query.authority) {
      const authKey = query.authority.toLowerCase().trim();
      apps = apps.filter(a => (a.authorityKey || '').toLowerCase() === authKey);
    }
    if (query.email) {
      const userEmail = query.email.toLowerCase().trim();
      apps = apps.filter(a => (a.email || '').toLowerCase() === userEmail);
    }

    return sendJson(res, 200, apps);
  }

  if (method === 'POST') {
    const getBody = (cb) => {
      if (req.body && typeof req.body === 'object') {
        return cb(req.body);
      }
      if (typeof req.body === 'string' && req.body.length > 0) {
        try { return cb(JSON.parse(req.body)); } catch(e) { return cb({}); }
      }
      let body = '';
      req.on('data', chunk => { body += chunk.toString(); });
      req.on('end', () => {
        try { cb(JSON.parse(body || '{}')); } catch(e) { cb({}); }
      });
    };

    getBody(async (payload) => {
      const item = payload || {};
      const pin = String(item.pincode || item.pin || '570001').trim();
      item.pin = pin;
      item.pincode = pin;
      item.status = item.status || 'Pending Inspection';
      item.lat = Number(item.lat) || 12.2958;
      item.lng = Number(item.lng) || 76.6394;
      item.gpsLocation = item.gpsLocation || `${item.lat}° N, ${item.lng}° E`;
      item.mapUrl = item.mapUrl || `https://www.google.com/maps?q=${item.lat},${item.lng}`;
      item.photos = Array.isArray(item.photos) && item.photos.length > 0 ? item.photos : (item.photo ? [item.photo] : []);
      item.photo = item.photo || (item.photos && item.photos[0]) || null;
      item.submittedAt = item.submittedAt || new Date().toISOString();

      // Dynamic PIN routing
      const GP_PINS = ['570026', '571130', '570028', '571311', '571201', '571186', '571101', '571120', '571124', '571125'];
      const TP_PINS = ['570018', '570017', '570027', '571607', '571604', '571602', '571610'];

      let resolvedAuthKey = '';
      let resolvedAuthName = '';
      let resolvedInspName = '';
      let resolvedInspEmail = '';
      let resolvedOfficerEmail = '';

      const isGp = GP_PINS.some(p => pin.startsWith(p) || p.startsWith(pin) || pin === p);
      const isTp = TP_PINS.some(p => pin.startsWith(p) || p.startsWith(pin) || pin === p);

      if (isGp) {
        resolvedAuthKey = 'gp';
        resolvedAuthName = 'Gram Panchayat (Bogadi Rural)';
        resolvedOfficerEmail = 'gp@gmail.com';
        if (pin === '571130') {
          resolvedInspName = 'Basavarajappa M.';
          resolvedInspEmail = 'basava.gp@gmail.com';
        } else if (pin === '571311') {
          resolvedInspName = 'S. Nanjappa';
          resolvedInspEmail = 'nanjappa.gp@gmail.com';
        } else if (pin === '570028') {
          resolvedInspName = 'Dimple';
          resolvedInspEmail = 'dim@gmail.com';
        } else {
          resolvedInspName = 'Seervi';
          resolvedInspEmail = 'q@gmail.com';
        }
      } else if (isTp) {
        resolvedAuthKey = 'tp';
        resolvedAuthName = 'Town Panchayat (Hootagalli Town)';
        resolvedOfficerEmail = 'tp@gmail.com';
        if (pin === '570017') {
          resolvedInspName = 'Manjunatha Rao';
          resolvedInspEmail = 'manju.tp@gmail.com';
        } else if (pin === '570027') {
          resolvedInspName = 'Prashanth G.';
          resolvedInspEmail = 'prashanth.tp@gmail.com';
        } else if (pin === '571607' || pin === '571604') {
          resolvedInspName = 'K. Suresh';
          resolvedInspEmail = 'suresh.tp@gmail.com';
        } else {
          resolvedInspName = 'M. Anand';
          resolvedInspEmail = 'anand.tp@gmail.com';
        }
      } else {
        resolvedAuthKey = 'mcc';
        resolvedAuthName = 'Mysuru Municipal Corporation (MCC Urban)';
        resolvedOfficerEmail = 'mcc@gmail.com';
        if (pin === '570002') {
          resolvedInspName = 'S. Swamy';
          resolvedInspEmail = 'swamy.mcc@gmail.com';
        } else if (pin === '570004') {
          resolvedInspName = 'Divya Shankar';
          resolvedInspEmail = 'divya.mcc@gmail.com';
        } else if (pin === '570023') {
          resolvedInspName = 'P. Ramesh';
          resolvedInspEmail = 'ramesh.mcc@gmail.com';
        } else {
          resolvedInspName = 'Rajesh Kumar';
          resolvedInspEmail = 'inspector.mcc@gmail.com';
        }
      }

      if (item.assignedInspectorEmail) {
        resolvedInspEmail = item.assignedInspectorEmail;
        resolvedInspName = item.assignedInspectorName || resolvedInspName;
        resolvedAuthKey = item.authorityKey || resolvedAuthKey;
        resolvedAuthName = item.authority || resolvedAuthName;
        resolvedOfficerEmail = item.assignedOfficerEmail || resolvedOfficerEmail;
      }

      const authPrefix = (resolvedAuthKey || 'mcc').toUpperCase();
      item.id = item.id || (`#${authPrefix}${new Date().getFullYear()}${Math.floor(100000 + Math.random() * 900000)}`);
      item.authorityKey = resolvedAuthKey;
      item.authority = resolvedAuthName;
      item.assignedInspectorName = resolvedInspName;
      item.assignedInspectorEmail = resolvedInspEmail;
      item.assignedOfficerEmail = resolvedOfficerEmail;

      if (supabase) {
        try {
          const mapped = mapAppToDb(item);
          await supabase.from('applications').upsert(mapped);
        } catch(e) {
          console.warn('Supabase upsert error in api/applications.js:', e);
        }
      }

      const inspId = 'INSP-' + (item.id.replace(/[^0-9]/g, '').slice(-4) || Math.floor(100 + Math.random() * 900));
      const inspectionRecord = {
        id: inspId,
        caseId: item.id,
        applicationId: item.id,
        applicantName: item.applicantName || 'Citizen',
        phone: item.phone || '',
        siteAddress: item.address || 'Mysuru Site',
        address: item.address || 'Mysuru Site',
        pin: item.pin,
        pincode: item.pincode,
        gpsLocation: item.gpsLocation,
        lat: item.lat,
        lng: item.lng,
        mapUrl: item.mapUrl,
        inspector: item.assignedInspectorName,
        assignedInspectorName: item.assignedInspectorName,
        assignedInspectorEmail: item.assignedInspectorEmail,
        authorityKey: item.authorityKey,
        authority: item.authority,
        date: item.inspectionTime ? new Date(item.inspectionTime).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' }) : ('Today, ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })),
        time: item.inspectionTime ? new Date(item.inspectionTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: item.status,
        photo: item.photo,
        photos: item.photos,
        propertyDetails: item.propertyId || 'Residential Site',
        tonnage: item.tonnage || '10 MT',
        inspectorNotes: item.inspectorNotes || '',
        documents: 'Khatta & Site Blueprint Validated'
      };

      return sendJson(res, 201, { success: true, item, inspection: inspectionRecord });
    });
  }
};
