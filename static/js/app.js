/**
 * Sistem Pengurusan Peminjaman Laptop
 * Frontend Application Logic (Vanilla JavaScript)
 */

document.addEventListener('DOMContentLoaded', () => {
    // State Aplikasi
    let currentView = 'dashboard';
    let recordsList = [];
    let pendingDeleteId = null;

    // Elemen Navigasi & Layout
    const navDashboard = document.getElementById('navDashboard');
    const navRecords = document.getElementById('navRecords');
    const viewDashboard = document.getElementById('viewDashboard');
    const viewRecords = document.getElementById('viewRecords');
    const pageSubtitle = document.getElementById('pageSubtitle');
    const navRecordBadge = document.getElementById('navRecordBadge');
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
    const btnQuickAdd = document.getElementById('btnQuickAdd');
    const btnOpenAddModal = document.getElementById('btnOpenAddModal');
    const btnEmptyAdd = document.getElementById('btnEmptyAdd');
    const btnViewAllFromDashboard = document.getElementById('btnViewAllFromDashboard');
    const liveDateText = document.getElementById('liveDateText');

    // Elemen Papan Pemuka
    const statTotalRecords = document.getElementById('statTotalRecords');
    const statTotalLaptops = document.getElementById('statTotalLaptops');
    const statTotalDepts = document.getElementById('statTotalDepts');
    const statMonthlyRecords = document.getElementById('statMonthlyRecords');
    const dashboardRecentList = document.getElementById('dashboardRecentList');
    const deptSummaryList = document.getElementById('deptSummaryList');

    // Elemen Tapisan & Jadual
    const searchInput = document.getElementById('searchInput');
    const btnClearSearch = document.getElementById('btnClearSearch');
    const filterDate = document.getElementById('filterDate');
    const btnResetFilter = document.getElementById('btnResetFilter');
    const recordsCountText = document.getElementById('recordsCountText');
    const activeFilterBadge = document.getElementById('activeFilterBadge');
    const recordsTableBody = document.getElementById('recordsTableBody');
    const emptyState = document.getElementById('emptyState');
    const emptyStateMessage = document.getElementById('emptyStateMessage');

    // Elemen Modal Tambah
    const addModal = document.getElementById('addModal');
    const addRecordForm = document.getElementById('addRecordForm');
    const btnCloseAddModal = document.getElementById('btnCloseAddModal');
    const btnCancelAdd = document.getElementById('btnCancelAdd');
    const addNamaLaptop = document.getElementById('addNamaLaptop');
    const addNamaJabatan = document.getElementById('addNamaJabatan');
    const addTarikhPeminjaman = document.getElementById('addTarikhPeminjaman');
    const addTujuan = document.getElementById('addTujuan');
    const errorAddLaptop = document.getElementById('errorAddLaptop');
    const errorAddJabatan = document.getElementById('errorAddJabatan');
    const errorAddTarikh = document.getElementById('errorAddTarikh');
    const errorAddTujuan = document.getElementById('errorAddTujuan');

    // Elemen Modal Edit
    const editModal = document.getElementById('editModal');
    const editRecordForm = document.getElementById('editRecordForm');
    const btnCloseEditModal = document.getElementById('btnCloseEditModal');
    const btnCancelEdit = document.getElementById('btnCancelEdit');
    const editRecordId = document.getElementById('editRecordId');
    const editRecordIdLabel = document.getElementById('editRecordIdLabel');
    const editNamaLaptop = document.getElementById('editNamaLaptop');
    const editNamaJabatan = document.getElementById('editNamaJabatan');
    const editTarikhPeminjaman = document.getElementById('editTarikhPeminjaman');
    const editTujuan = document.getElementById('editTujuan');
    const errorEditLaptop = document.getElementById('errorEditLaptop');
    const errorEditJabatan = document.getElementById('errorEditJabatan');
    const errorEditTarikh = document.getElementById('errorEditTarikh');
    const errorEditTujuan = document.getElementById('errorEditTujuan');

    // Elemen Modal Padam
    const deleteModal = document.getElementById('deleteModal');
    const btnCloseDeleteModal = document.getElementById('btnCloseDeleteModal');
    const btnCancelDelete = document.getElementById('btnCancelDelete');
    const btnConfirmDelete = document.getElementById('btnConfirmDelete');
    const deleteSummaryId = document.getElementById('deleteSummaryId');
    const deleteSummaryLaptop = document.getElementById('deleteSummaryLaptop');
    const deleteSummaryJabatan = document.getElementById('deleteSummaryJabatan');
    const deleteSummaryTarikh = document.getElementById('deleteSummaryTarikh');

    // Toast Container
    const toastContainer = document.getElementById('toastContainer');

    /* ==========================================================================
       1. Format Tarikh & Utiliti
       ========================================================================== */
    function getTodayDateString() {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        return `${yyyy}-${mm}-${dd}`;
    }

    function formatDateDisplay(dateStr) {
        if (!dateStr) return '-';
        try {
            const parts = dateStr.split('-');
            if (parts.length === 3) {
                return `${parts[2]}/${parts[1]}/${parts[0]}`;
            }
            return dateStr;
        } catch (e) {
            return dateStr;
        }
    }

    function updateLiveHeaderDate() {
        const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        const now = new Date();
        const formatted = now.toLocaleDateString('ms-MY', options);
        liveDateText.textContent = formatted;
    }

    function escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.toString().replace(/[&<>"']/g, (m) => map[m]);
    }

    /* ==========================================================================
       2. Notifikasi Toast
       ========================================================================== */
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        let iconSvg = '';
        if (type === 'success') {
            iconSvg = `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>`;
        } else if (type === 'error') {
            iconSvg = `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>`;
        } else {
            iconSvg = `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>`;
        }

        toast.innerHTML = `
            ${iconSvg}
            <div class="toast-message">${escapeHtml(message)}</div>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(40px)';
            setTimeout(() => {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 300);
        }, 3500);
    }

    /* ==========================================================================
       3. Navigasi Antara Halaman (Papan Pemuka vs Rekod)
       ========================================================================== */
    function switchView(viewName) {
        currentView = viewName;
        if (viewName === 'dashboard') {
            navDashboard.classList.add('active');
            navRecords.classList.remove('active');
            viewDashboard.classList.add('active');
            viewRecords.classList.remove('active');
            pageSubtitle.textContent = 'Papan Pemuka & Statistik Keseluruhan';
            loadDashboardStats();
        } else {
            navDashboard.classList.remove('active');
            navRecords.classList.add('active');
            viewDashboard.classList.remove('active');
            viewRecords.classList.add('active');
            pageSubtitle.textContent = 'Senarai & Pengurusan Rekod Peminjaman';
            loadRecords();
        }
        // Tutup menu sidebar pada peranti mudah alih jika dibuka
        sidebar.classList.remove('open');
    }

    navDashboard.addEventListener('click', () => switchView('dashboard'));
    navRecords.addEventListener('click', () => switchView('records'));
    if (btnViewAllFromDashboard) {
        btnViewAllFromDashboard.addEventListener('click', () => switchView('records'));
    }

    // Toggle menu mudah alih
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
    if (sidebarCloseBtn) {
        sidebarCloseBtn.addEventListener('click', () => {
            sidebar.classList.remove('open');
        });
    }

    /* ==========================================================================
       4. Papan Pemuka: Muat Data Statistik & Aktiviti Terkini
       ========================================================================== */
    async function loadDashboardStats() {
        try {
            const res = await fetch('/api/dashboard/stats');
            const data = await res.json();
            if (data.success) {
                const stats = data.data;
                statTotalRecords.textContent = stats.total_records;
                statTotalLaptops.textContent = stats.total_laptops;
                statTotalDepts.textContent = stats.total_departments;
                statMonthlyRecords.textContent = stats.monthly_records;
                navRecordBadge.textContent = stats.total_records;

                // Paparkan 5 aktiviti terkini
                renderRecentActivities(stats.recent_activities);

                // Paparkan ringkasan jabatan
                renderDepartmentSummary(stats.department_summary, stats.total_records);
            }
        } catch (error) {
            console.error('Ralat memuatkan statistik:', error);
            showToast('Gagal memuatkan statistik papan pemuka.', 'error');
        }
    }

    function renderRecentActivities(activities) {
        if (!activities || activities.length === 0) {
            dashboardRecentList.innerHTML = `
                <tr>
                    <td colspan="5" class="table-loading">Tiada rekod peminjaman didaftarkan lagi.</td>
                </tr>
            `;
            return;
        }

        dashboardRecentList.innerHTML = activities.map(rec => `
            <tr>
                <td><span class="badge-id">#${rec.id}</span></td>
                <td>
                    <div class="laptop-cell">
                        <svg class="laptop-cell-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                            <line x1="8" y1="21" x2="16" y2="21"></line>
                            <line x1="12" y1="17" x2="12" y2="21"></line>
                        </svg>
                        ${escapeHtml(rec.nama_laptop)}
                    </div>
                </td>
                <td><span class="dept-badge">${escapeHtml(rec.nama_jabatan)}</span></td>
                <td>
                    <div class="date-pill">
                        <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                        </svg>
                        ${formatDateDisplay(rec.tarikh_peminjaman)}
                    </div>
                </td>
                <td><span class="purpose-text" title="${escapeHtml(rec.tujuan)}">${escapeHtml(rec.tujuan)}</span></td>
            </tr>
        `).join('');
    }

    function renderDepartmentSummary(deptList, totalRecords) {
        if (!deptList || deptList.length === 0) {
            deptSummaryList.innerHTML = '<div class="table-loading">Tiada data peminjaman jabatan.</div>';
            return;
        }

        const maxCount = Math.max(...deptList.map(d => d.count), 1);

        deptSummaryList.innerHTML = deptList.map(d => {
            const percentage = Math.round((d.count / (totalRecords || 1)) * 100);
            const barWidth = Math.round((d.count / maxCount) * 100);
            return `
                <div class="dept-item">
                    <div class="dept-item-header">
                        <span class="dept-name">${escapeHtml(d.nama_jabatan)}</span>
                        <span class="dept-count">${d.count} (${percentage}%)</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-bar-fill" style="width: ${barWidth}%"></div>
                    </div>
                </div>
            `;
        }).join('');
    }

    /* ==========================================================================
       5. Rekod Peminjaman: Muat, Papar, Tapis & Carian
       ========================================================================== */
    async function loadRecords() {
        const search = searchInput.value.trim();
        const date = filterDate.value.trim();

        // Kemaskini butang kosongkan carian
        if (search) {
            btnClearSearch.style.display = 'block';
        } else {
            btnClearSearch.style.display = 'none';
        }

        // Tunjukkan indikator penapis aktif
        if (search || date) {
            activeFilterBadge.style.display = 'inline-block';
        } else {
            activeFilterBadge.style.display = 'none';
        }

        recordsTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="table-loading">Memuatkan data rekod...</td>
            </tr>
        `;
        emptyState.style.display = 'none';

        try {
            const params = new URLSearchParams();
            if (search) params.append('search', search);
            if (date) params.append('date', date);

            const res = await fetch(`/api/records?${params.toString()}`);
            const data = await res.json();

            if (data.success) {
                recordsList = data.records;
                renderRecordsTable(recordsList);
                recordsCountText.textContent = `Menunjukkan ${recordsList.length} rekod`;
                navRecordBadge.textContent = recordsList.length;
            } else {
                showToast(data.message || 'Gagal memuatkan rekod.', 'error');
            }
        } catch (error) {
            console.error('Ralat memuatkan rekod:', error);
            showToast('Ralat sambungan ke pangkalan data.', 'error');
        }
    }

    function renderRecordsTable(records) {
        if (!records || records.length === 0) {
            recordsTableBody.innerHTML = '';
            emptyState.style.display = 'block';
            if (searchInput.value || filterDate.value) {
                emptyStateMessage.textContent = 'Tiada rekod yang sepadan dengan carian atau penapis tarikh anda.';
            } else {
                emptyStateMessage.textContent = 'Belum ada rekod peminjaman didaftarkan.';
            }
            return;
        }

        emptyState.style.display = 'none';
        recordsTableBody.innerHTML = records.map(rec => `
            <tr data-id="${rec.id}">
                <td><span class="badge-id">#${rec.id}</span></td>
                <td>
                    <div class="laptop-cell">
                        <svg class="laptop-cell-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                            <line x1="8" y1="21" x2="16" y2="21"></line>
                            <line x1="12" y1="17" x2="12" y2="21"></line>
                        </svg>
                        <strong>${escapeHtml(rec.nama_laptop)}</strong>
                    </div>
                </td>
                <td><span class="dept-badge">${escapeHtml(rec.nama_jabatan)}</span></td>
                <td>
                    <div class="date-pill">
                        <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                        </svg>
                        ${formatDateDisplay(rec.tarikh_peminjaman)}
                    </div>
                </td>
                <td><div class="purpose-text" title="${escapeHtml(rec.tujuan)}">${escapeHtml(rec.tujuan)}</div></td>
                <td>
                    <div class="table-actions">
                        <button type="button" class="btn btn-action-edit" data-action="edit" data-id="${rec.id}">
                            <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                            </svg>
                            <span>Edit</span>
                        </button>
                        <button type="button" class="btn btn-action-delete" data-action="delete" data-id="${rec.id}">
                            <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none">
                                <polyline points="3 6 5 6 21 6"></polyline>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                            <span>Padam</span>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    // Debounce Carian Pantas
    let searchTimeout = null;
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadRecords();
        }, 300);
    });

    btnClearSearch.addEventListener('click', () => {
        searchInput.value = '';
        btnClearSearch.style.display = 'none';
        loadRecords();
    });

    filterDate.addEventListener('change', () => {
        loadRecords();
    });

    btnResetFilter.addEventListener('click', () => {
        searchInput.value = '';
        filterDate.value = '';
        btnClearSearch.style.display = 'none';
        loadRecords();
    });

    /* ==========================================================================
       6. Tambah Rekod Baharu (Add Modal)
       ========================================================================== */
    function openAddModal() {
        addRecordForm.reset();
        addTarikhPeminjaman.value = getTodayDateString();
        clearValidationErrors([errorAddLaptop, errorAddJabatan, errorAddTarikh, errorAddTujuan]);
        addNamaLaptop.classList.remove('input-error');
        addNamaJabatan.classList.remove('input-error');
        addTarikhPeminjaman.classList.remove('input-error');
        addTujuan.classList.remove('input-error');
        addModal.classList.add('active');
        setTimeout(() => addNamaLaptop.focus(), 150);
    }

    function closeAddModal() {
        addModal.classList.remove('active');
    }

    btnQuickAdd.addEventListener('click', openAddModal);
    btnOpenAddModal.addEventListener('click', openAddModal);
    if (btnEmptyAdd) {
        btnEmptyAdd.addEventListener('click', openAddModal);
    }
    btnCloseAddModal.addEventListener('click', closeAddModal);
    btnCancelAdd.addEventListener('click', closeAddModal);

    addRecordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearValidationErrors([errorAddLaptop, errorAddJabatan, errorAddTarikh, errorAddTujuan]);

        const nama_laptop = addNamaLaptop.value.trim();
        const nama_jabatan = addNamaJabatan.value.trim();
        const tarikh_peminjaman = addTarikhPeminjaman.value.trim();
        const tujuan = addTujuan.value.trim();

        let hasError = false;

        if (!nama_laptop) {
            showFieldError(errorAddLaptop, addNamaLaptop, 'Sila masukkan nama atau model laptop.');
            hasError = true;
        }
        if (!nama_jabatan) {
            showFieldError(errorAddJabatan, addNamaJabatan, 'Sila masukkan nama jabatan peminjam.');
            hasError = true;
        }
        if (!tarikh_peminjaman) {
            showFieldError(errorAddTarikh, addTarikhPeminjaman, 'Sila pilih tarikh peminjaman.');
            hasError = true;
        }
        if (!tujuan) {
            showFieldError(errorAddTujuan, addTujuan, 'Sila nyatakan tujuan peminjaman laptop.');
            hasError = true;
        }

        if (hasError) return;

        try {
            const res = await fetch('/api/records', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan })
            });

            const result = await res.json();
            if (res.ok && result.success) {
                closeAddModal();
                showToast(result.message || 'Rekod peminjaman berjaya ditambah.', 'success');
                loadDashboardStats();
                if (currentView === 'records') {
                    loadRecords();
                } else {
                    switchView('records');
                }
            } else {
                showToast(result.message || 'Gagal menyimpan rekod peminjaman.', 'error');
            }
        } catch (error) {
            console.error('Ralat simpan rekod:', error);
            showToast('Ralat berlaku semasa menyambung ke pelayan.', 'error');
        }
    });

    /* ==========================================================================
       7. Kemaskini Rekod (Edit Modal)
       ========================================================================== */
    async function openEditModal(recordId) {
        clearValidationErrors([errorEditLaptop, errorEditJabatan, errorEditTarikh, errorEditTujuan]);
        editNamaLaptop.classList.remove('input-error');
        editNamaJabatan.classList.remove('input-error');
        editTarikhPeminjaman.classList.remove('input-error');
        editTujuan.classList.remove('input-error');

        try {
            const res = await fetch(`/api/records/${recordId}`);
            const data = await res.json();

            if (data.success && data.record) {
                const rec = data.record;
                editRecordId.value = rec.id;
                editRecordIdLabel.textContent = rec.id;
                editNamaLaptop.value = rec.nama_laptop;
                editNamaJabatan.value = rec.nama_jabatan;
                editTarikhPeminjaman.value = rec.tarikh_peminjaman;
                editTujuan.value = rec.tujuan;

                editModal.classList.add('active');
                setTimeout(() => editNamaLaptop.focus(), 150);
            } else {
                showToast(data.message || 'Rekod tidak dijumpai.', 'error');
            }
        } catch (error) {
            console.error('Ralat dapatkan rekod:', error);
            showToast('Gagal memuatkan maklumat rekod untuk dikemaskini.', 'error');
        }
    }

    function closeEditModal() {
        editModal.classList.remove('active');
    }

    btnCloseEditModal.addEventListener('click', closeEditModal);
    btnCancelEdit.addEventListener('click', closeEditModal);

    editRecordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearValidationErrors([errorEditLaptop, errorEditJabatan, errorEditTarikh, errorEditTujuan]);

        const recordId = editRecordId.value;
        const nama_laptop = editNamaLaptop.value.trim();
        const nama_jabatan = editNamaJabatan.value.trim();
        const tarikh_peminjaman = editTarikhPeminjaman.value.trim();
        const tujuan = editTujuan.value.trim();

        let hasError = false;

        if (!nama_laptop) {
            showFieldError(errorEditLaptop, editNamaLaptop, 'Sila masukkan nama atau model laptop.');
            hasError = true;
        }
        if (!nama_jabatan) {
            showFieldError(errorEditJabatan, editNamaJabatan, 'Sila masukkan nama jabatan peminjam.');
            hasError = true;
        }
        if (!tarikh_peminjaman) {
            showFieldError(errorEditTarikh, editTarikhPeminjaman, 'Sila pilih tarikh peminjaman.');
            hasError = true;
        }
        if (!tujuan) {
            showFieldError(errorEditTujuan, editTujuan, 'Sila nyatakan tujuan peminjaman laptop.');
            hasError = true;
        }

        if (hasError) return;

        try {
            const res = await fetch(`/api/records/${recordId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan })
            });

            const result = await res.json();
            if (res.ok && result.success) {
                closeEditModal();
                showToast(result.message || 'Rekod peminjaman berjaya dikemaskini.', 'success');
                loadDashboardStats();
                if (currentView === 'records') {
                    loadRecords();
                }
            } else {
                showToast(result.message || 'Gagal mengemaskini rekod peminjaman.', 'error');
            }
        } catch (error) {
            console.error('Ralat kemaskini rekod:', error);
            showToast('Ralat berlaku semasa mengemaskini rekod.', 'error');
        }
    });

    /* ==========================================================================
       8. Padam Rekod (Delete Modal)
       ========================================================================== */
    function openDeleteModal(recordId) {
        const record = recordsList.find(r => r.id === parseInt(recordId, 10));
        pendingDeleteId = recordId;

        if (record) {
            deleteSummaryId.textContent = `#${record.id}`;
            deleteSummaryLaptop.textContent = record.nama_laptop;
            deleteSummaryJabatan.textContent = record.nama_jabatan;
            deleteSummaryTarikh.textContent = formatDateDisplay(record.tarikh_peminjaman);
        } else {
            deleteSummaryId.textContent = `#${recordId}`;
            deleteSummaryLaptop.textContent = '-';
            deleteSummaryJabatan.textContent = '-';
            deleteSummaryTarikh.textContent = '-';
        }

        deleteModal.classList.add('active');
    }

    function closeDeleteModal() {
        deleteModal.classList.remove('active');
        pendingDeleteId = null;
    }

    btnCloseDeleteModal.addEventListener('click', closeDeleteModal);
    btnCancelDelete.addEventListener('click', closeDeleteModal);

    btnConfirmDelete.addEventListener('click', async () => {
        if (!pendingDeleteId) return;

        try {
            const res = await fetch(`/api/records/${pendingDeleteId}`, {
                method: 'DELETE'
            });

            const result = await res.json();
            if (res.ok && result.success) {
                closeDeleteModal();
                showToast(result.message || 'Rekod peminjaman berjaya dipadam.', 'success');
                loadDashboardStats();
                loadRecords();
            } else {
                showToast(result.message || 'Gagal memadam rekod peminjaman.', 'error');
            }
        } catch (error) {
            console.error('Ralat padam rekod:', error);
            showToast('Ralat berlaku semasa memadam rekod.', 'error');
        }
    });

    /* ==========================================================================
       9. Delegasi Acara Jadual (Edit & Padam Butang)
       ========================================================================== */
    recordsTableBody.addEventListener('click', (e) => {
        const actionBtn = e.target.closest('button[data-action]');
        if (!actionBtn) return;

        const action = actionBtn.getAttribute('data-action');
        const id = actionBtn.getAttribute('data-id');

        if (action === 'edit') {
            openEditModal(id);
        } else if (action === 'delete') {
            openDeleteModal(id);
        }
    });

    /* ==========================================================================
       10. Pembantu Pengesahan Borang
       ========================================================================== */
    function showFieldError(errorElement, inputElement, message) {
        errorElement.textContent = message;
        errorElement.classList.add('visible');
        inputElement.classList.add('input-error');
    }

    function clearValidationErrors(errorElements) {
        errorElements.forEach(el => {
            el.textContent = '';
            el.classList.remove('visible');
        });
    }

    // Buang ralat merah serta-merta apabila pengguna mula menaip semula
    [addNamaLaptop, addNamaJabatan, addTarikhPeminjaman, addTujuan].forEach(input => {
        input.addEventListener('input', () => {
            input.classList.remove('input-error');
            const err = input.parentElement.querySelector('.field-error');
            if (err) err.classList.remove('visible');
        });
    });

    [editNamaLaptop, editNamaJabatan, editTarikhPeminjaman, editTujuan].forEach(input => {
        input.addEventListener('input', () => {
            input.classList.remove('input-error');
            const err = input.parentElement.querySelector('.field-error');
            if (err) err.classList.remove('visible');
        });
    });

    // Tutup modal apabila klik di luar kawasan modal (overlay)
    [addModal, editModal, deleteModal].forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });

    // Tutup modal dengan kekunci Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAddModal();
            closeEditModal();
            closeDeleteModal();
        }
    });

    /* ==========================================================================
       11. Permulaan Aplikasi (Init)
       ========================================================================== */
    updateLiveHeaderDate();
    loadDashboardStats();
});
