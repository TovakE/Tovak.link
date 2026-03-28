const form = document.getElementById('recordForm');
const output = document.getElementById('output');
const statusText = document.getElementById('status');
const downloadJsonBtn = document.getElementById('downloadJson');
const downloadTxtBtn = document.getElementById('downloadTxt');

const requiredFields = ['name', 'address', 'phone'];
let latestRecord = null;

function normalizePhone(phone) {
  const digits = phone.replace(/\D+/g, '');
  if (digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
  }
  if (digits.length === 11 && digits.startsWith('1')) {
    return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
  }
  return digits || phone.trim();
}

function validateAndCollect() {
  const person = {};
  let valid = true;

  requiredFields.forEach((fieldName) => {
    const input = form.elements[fieldName];
    const error = document.getElementById(`${fieldName}Error`);
    const value = input.value.trim();

    if (!value) {
      valid = false;
      input.classList.add('is-invalid');
      error.textContent = `${fieldName[0].toUpperCase()}${fieldName.slice(1)} is required.`;
    } else {
      input.classList.remove('is-invalid');
      error.textContent = '';
      person[fieldName] = fieldName === 'phone' ? normalizePhone(value) : value;
    }
  });

  const email = form.elements.email.value.trim();
  const notes = form.elements.notes.value.trim();

  if (email) person.email = email;
  if (notes) person.notes = notes;

  return { valid, person };
}

function buildRecord(person) {
  const now = new Date();
  const timestamp = now.getTime();
  const suffix = Math.random().toString(36).slice(2, 8);

  return {
    id: `${timestamp}-${suffix}`,
    createdAt: now.toISOString(),
    person,
  };
}

function getFilename(ext) {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  const date = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}`;
  const time = `${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
  return `record-${date}-${time}.${ext}`;
}

function downloadContent(content, type, extension) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = getFilename(extension);
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);

  statusText.textContent = `Export complete: ${link.download}`;
  statusText.classList.add('success');
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  statusText.textContent = '';
  statusText.classList.remove('success');

  const { valid, person } = validateAndCollect();
  if (!valid) {
    output.textContent = 'Please fix validation errors before generating output.';
    downloadJsonBtn.disabled = true;
    downloadTxtBtn.disabled = true;
    return;
  }

  latestRecord = buildRecord(person);
  output.textContent = JSON.stringify(latestRecord, null, 2);

  downloadJsonBtn.disabled = false;
  downloadTxtBtn.disabled = false;
});

downloadJsonBtn.addEventListener('click', () => {
  if (!latestRecord) return;
  downloadContent(JSON.stringify(latestRecord, null, 2), 'application/json', 'json');
});

downloadTxtBtn.addEventListener('click', () => {
  if (!latestRecord) return;
  const lines = [
    `ID: ${latestRecord.id}`,
    `Created At: ${latestRecord.createdAt}`,
    `Name: ${latestRecord.person.name}`,
    `Address: ${latestRecord.person.address}`,
    `Phone: ${latestRecord.person.phone}`,
  ];
  if (latestRecord.person.email) lines.push(`Email: ${latestRecord.person.email}`);
  if (latestRecord.person.notes) lines.push(`Notes: ${latestRecord.person.notes}`);

  downloadContent(lines.join('\n'), 'text/plain', 'txt');
});
