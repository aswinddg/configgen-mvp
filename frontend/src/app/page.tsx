'use client';

import { useState, useEffect, useMemo } from 'react';

interface Vendor {
  id: number;
  name: string;
}

interface Scenario {
  id: number;
  vendor_id: number;
  name: string;
  description: string;
}

interface Param {
  id: number;
  scenario_id: number;
  key: string;
  label: string;
  type: string;
  required: boolean;
  default_value: string;
  options?: string;
}

export default function Home() {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [params, setParams] = useState<Param[]>([]);
  const [selectedVendor, setSelectedVendor] = useState<number | null>(null);
  const [selectedScenario, setSelectedScenario] = useState<number | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [formDataReady, setFormDataReady] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadVendors = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/vendors');
        const vendorsData = await response.json();
        setVendors(vendorsData);
      } catch (error) {
        console.error('Error loading vendors:', error);
      }
    };
    loadVendors();
  }, []);

  useEffect(() => {
    if (selectedVendor) {
      const loadScenarios = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/scenarios');
          const scenariosData = await response.json();
          const filteredScenarios = scenariosData.filter((s: Scenario) => s.vendor_id === selectedVendor);
          setScenarios(filteredScenarios);
          setSelectedScenario(null);
          setParams([]);
        } catch (error) {
          console.error('Error loading scenarios:', error);
        }
      };
      loadScenarios();
    }
  }, [selectedVendor]);

  useEffect(() => {
    if (selectedScenario) {
      const loadParams = async () => {
        try {
          const response = await fetch(`http://localhost:8000/api/scenarios/${selectedScenario}/params`);
          const paramsData = await response.json();
          setParams(paramsData);
          const initialData: Record<string, string> = {};
          paramsData.forEach((param: Param) => {
            initialData[param.key] = param.default_value || '';
          });
          setFormData(initialData);
          setFormDataReady(true);
          console.log('✅ FORM DATA READY - initialData:', initialData);
        } catch (error) {
          console.error('Error loading params:', error);
        }
      };
      loadParams();
    }
  }, [selectedScenario]);

  const handleGenerate = async () => {
    if (!selectedScenario) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scenario_id: selectedScenario,
          params: formData
        }),
      });

      if (response.ok) {
        const blob = await response.blob();

        // Extract filename from Content-Disposition header
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `config-${Date.now()}.txt`;

        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
          if (filenameMatch && filenameMatch[1]) {
            filename = filenameMatch[1];
          }
        }

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert('Error generando configuración');
      }
    } catch (error) {
      console.error('Error generating config:', error);
      alert('Error generando configuración');
    } finally {
      setLoading(false);
    }
  };



  const CompletionBadge = ({ active }: { active: boolean }) => (
    <span className={`inline-flex h-2.5 w-2.5 rounded-full ${active ? 'bg-emerald-400' : 'bg-white/40'}`} />
  );

  const renderParamInput = (param: Param) => {
    const optionList =
      param.options
        ?.split(',')
        .map(option => option.trim())
        .filter(Boolean) || [];

    const shouldRenderSelect =
      optionList.length > 0 &&
      (param.type === 'select' || param.key === 'wan_interface');

    if (shouldRenderSelect) {
      return (
        <select
          className="w-full rounded-xl border border-white/20 bg-slate-900/50 p-3 text-white focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-400/50"
          value={formData[param.key] || ''}
          onChange={(e) => {
            console.log(`CHANGE ${param.key} -> ${e.target.value}`);
            const newValue = e.target.value;
            setFormData(prev => {
              const updated = { ...prev, [param.key]: newValue };
              // Si cambia wan_interface, actualizar nat_outside automáticamente
              if (param.key === 'wan_interface' && newValue) {
                updated['nat_outside'] = newValue;
              }
              // Si cambia lan_interface, actualizar nat_inside automáticamente
              if (param.key === 'lan_interface' && newValue) {
                updated['nat_inside'] = newValue;
              }
              return updated;
            });
          }}
        >
          <option value="">-- Seleccionar {param.label} --</option>
          {optionList.map(option => (
            <option key={option} value={option} className="text-slate-900">
              {option}
            </option>
          ))}
        </select>
      );
    }

    return (
      <input
        type={param.type === 'ip' ? 'text' : param.type}
        className="w-full rounded-xl border border-white/20 bg-slate-900/50 p-3 text-white placeholder-white/40 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-400/50"
        placeholder={param.default_value || `Ingrese ${param.label.toLowerCase()}`}
        value={formData[param.key] || ''}
        onChange={(e) =>
          setFormData(prev => ({
            ...prev,
            [param.key]: e.target.value
          }))
        }
      />
    );
  };

  const visibleParams = useMemo(() => {
    console.log('🔍 VISIBILITY CHECK - formDataReady:', formDataReady, 'params.length:', params.length);
    if (!params.length || !formDataReady) return [];

    const filtered = params.filter(param => {
      const key = param.key.trim();

      // --- WAN LOGIC ---
      const wanEnabled = (formData['wan_enabled'] || 'Yes').trim();

      // If WAN is disabled, hide ALL WAN related fields
      if (wanEnabled === 'No') {
        const wanFields = ['wan_interface', 'wan_type', 'wan_ip', 'wan_mask', 'gateway', 'dns1'];
        if (wanFields.includes(key)) return false;
      }

      // If WAN is enabled, check WAN Type specific visibility
      if (wanEnabled === 'Yes') {
        const wanType = (formData['wan_type'] || '').trim();
        // If DHCP, hide Static IP fields
        if (wanType === 'DHCP') {
          const staticFields = ['wan_ip', 'wan_mask', 'gateway'];
          if (staticFields.includes(key)) return false;
        }
      }

      // --- LAN LOGIC ---
      const lanEnabled = (formData['lan_enabled'] || 'Yes').trim();

      // If LAN is disabled, hide ALL LAN related fields
      if (lanEnabled === 'No') {
        const lanFields = ['lan_type', 'lan_interface_name', 'bridge_ports', 'lan_interface', 'lan_ip', 'lan_mask', 'lan_network'];
        if (lanFields.includes(key)) return false;
      }

      // If LAN is enabled, check LAN Type specific visibility
      if (lanEnabled === 'Yes') {
        const lanType = (formData['lan_type'] || '').trim();

        if (lanType === 'Bridge') {
          if (['lan_interface'].includes(key)) return false;
        } else if (lanType === 'Interface') {
          if (['bridge_ports'].includes(key)) return false;
        } else if (lanType === 'VLAN') {
          if (['bridge_ports', 'lan_interface_name'].includes(key)) return false;
        } else {
          // If no type selected or other, maybe hide specific fields?
          // For now, keep default behavior
          if (['bridge_ports'].includes(key)) return false; // Hide bridge ports by default if not Bridge
        }
      }

      // --- DHCP SERVER LOGIC ---
      const dhcpEnabled = (formData['dhcp_server_enabled'] || 'Yes').trim();
      if (dhcpEnabled === 'No') {
        const dhcpFields = ['dhcp_pool_start', 'dhcp_pool_end', 'dhcp_lease_time', 'dns_servers'];
        if (dhcpFields.includes(key)) return false;
      }

      // --- NAT LOGIC ---
      // NAT only makes sense when WAN is enabled
      if (key === 'enable_nat' && wanEnabled === 'No') {
        return false;
      }

      // NAT Configuration Fields - Show only when enable_nat is "Yes" AND WAN is enabled
      const natConfigFields = ['nat_inside', 'nat_outside', 'nat_inside_source_static', 'nat_pool', 'nat_inside_source_list'];
      if (natConfigFields.includes(key)) {
        if (wanEnabled === 'No') return false;
        const natEnabled = (formData['enable_nat'] || 'No').trim();
        return natEnabled === 'Yes';
      }

      return true;
    });

    console.log('✅ VISIBLE PARAMS COUNT:', filtered.length, 'out of', params.length);
    return filtered;
  }, [params, formData, formDataReady]);

  const areParamsValid = () => {
    if (visibleParams.length === 0) return false;
    return visibleParams.every(param => {
      if (!param.required) return true;
      const value = formData[param.key];
      return value && value.trim() !== '';
    });
  };

  const steps = [
    { id: 1, label: 'Vendor', active: Boolean(selectedVendor) },
    { id: 2, label: 'Escenario', active: Boolean(selectedScenario) },
    { id: 3, label: 'Parámetros', active: areParamsValid() },
    { id: 4, label: 'Descarga', active: areParamsValid() && !loading }
  ];

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-50">
      <div className="absolute inset-0 opacity-70">
        <div className="absolute -left-24 top-10 h-80 w-80 rounded-full bg-violet-600/30 blur-[120px]" />
        <div className="absolute right-0 top-0 h-96 w-96 rounded-full bg-sky-500/40 blur-[150px]" />
        <div className="absolute bottom-0 left-1/2 h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-emerald-500/20 blur-[200px]" />
      </div>

      <main className="relative mx-auto flex max-w-5xl flex-col gap-10 px-6 pb-16 pt-14 lg:pt-20">


        <section className="space-y-6 text-center">
          <p className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1 text-xs uppercase tracking-[0.2em] text-white/70">
            ConfigGen · MVP
          </p>
          <div className="space-y-4">
            <h1 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl">
              Diseña configuraciones de red en minutos
            </h1>
            <p className="mx-auto max-w-2xl text-base text-white/70 sm:text-lg">
              Selecciona un vendor, define un escenario y deja que la app genere archivos listos para desplegar.
              Menos clics, menos scripts manuales, más tiempo para tareas estratégicas.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-white/70 sm:text-base">
            <span className="rounded-full border border-white/10 px-4 py-2">Multi-vendor</span>
            <span className="rounded-full border border-white/10 px-4 py-2">Validación guiada</span>
            <span className="rounded-full border border-white/10 px-4 py-2">Descarga instantánea</span>
          </div>
        </section>

        <section className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-indigo-900/20 backdrop-blur-xl sm:p-8">
          <header className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-white/50">Flujo guiado</p>
              <h2 className="text-2xl font-semibold text-white">Construye tu configuración</h2>
            </div>
            <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/70">
              <div className="flex items-center gap-2">
                <span className="text-lg">⚡</span>
                <span>{visibleParams.length} parámetros activos</span>
              </div>
            </div>
          </header>

          <ol className="mb-8 grid gap-4 text-sm text-white/60 sm:grid-cols-4">
            {steps.map(step => (
              <li
                key={step.id}
                className={`flex flex-col gap-2 rounded-2xl border border-white/10 px-4 py-3 ${step.active ? 'bg-white/10 text-white' : 'bg-transparent'
                  }`}
              >
                <div className="flex items-center justify-between text-xs uppercase tracking-[0.25em]">
                  Paso {step.id}
                  <CompletionBadge active={step.active} />
                </div>
                <span className="text-base font-medium">{step.label}</span>
              </li>
            ))}
          </ol>

          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-5 shadow-lg shadow-black/30">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-white/40">Paso 1</p>
                  <h3 className="text-lg font-semibold text-white">Selecciona el Vendor</h3>
                </div>
                <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-white/70">
                  {vendors.length} disponibles
                </span>
              </div>
              <select
                className="w-full rounded-xl border border-white/20 bg-white/10 p-3 text-white placeholder-white/40 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-400/50"
                value={selectedVendor || ''}
                onChange={(e) => setSelectedVendor(Number(e.target.value) || null)}
              >
                <option value="">-- Seleccionar Vendor --</option>
                {vendors.map(vendor => (
                  <option key={vendor.id} value={vendor.id} className="text-slate-900">
                    {vendor.name}
                  </option>
                ))}
              </select>
            </div>

            <div
              className={`rounded-2xl border border-white/10 p-5 shadow-lg shadow-black/30 ${selectedVendor ? 'bg-slate-900/60' : 'bg-slate-900/20'
                }`}
            >
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-white/40">Paso 2</p>
                  <h3 className="text-lg font-semibold text-white">Escoge el Escenario</h3>
                </div>
                {selectedVendor ? (
                  <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-white/70">
                    {scenarios.length} opciones
                  </span>
                ) : (
                  <span className="text-xs text-white/40">Activa el paso anterior</span>
                )}
              </div>
              <select
                className="w-full rounded-xl border border-white/20 bg-white/10 p-3 text-white placeholder-white/40 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-400/50 disabled:opacity-40"
                value={selectedScenario || ''}
                onChange={(e) => setSelectedScenario(Number(e.target.value) || null)}
                disabled={!selectedVendor}
              >
                <option value="">-- Seleccionar Escenario --</option>
                {scenarios.map(scenario => (
                  <option key={scenario.id} value={scenario.id} className="text-slate-900">
                    {scenario.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mt-8 rounded-2xl border border-white/10 bg-slate-900/70 p-6 shadow-lg shadow-black/30">
            <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-white/40">Paso 3</p>
                <h3 className="text-xl font-semibold text-white">Define los parámetros</h3>
              </div>
              {!params.length && (
                <p className="text-sm text-white/60">
                  Selecciona un escenario para desbloquear los campos configurables.
                </p>
              )}
            </div>

            {visibleParams.length > 0 && (
              <div className="grid gap-5">
                {visibleParams.map(param => (
                  <div
                    key={param.id}
                    className="rounded-xl border border-white/10 bg-white/5 p-4 transition hover:border-sky-400/60 hover:bg-white/10"
                  >
                    <label className="mb-2 flex items-center justify-between text-sm font-medium text-white">
                      <span>
                        {param.label}{param.required && <span className="ml-1 text-rose-300">*</span>}
                      </span>
                      <span className="text-xs text-white/50">Tipo: {param.type}</span>
                    </label>
                    {renderParamInput(param)}
                  </div>
                ))}
              </div>
            )}
          </div>

          {visibleParams.length > 0 && (
            <div className="mt-8 flex flex-col gap-4 rounded-2xl border border-white/10 bg-gradient-to-r from-sky-600/80 to-indigo-600/80 p-6 shadow-xl shadow-sky-900/30 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-white/70">Listo para generar</p>
                <h4 className="text-2xl font-semibold text-white">Tu config está validada</h4>
                <p className="text-white/80">Pulsa el botón para descargar el archivo automático.</p>
              </div>
              <button
                onClick={handleGenerate}
                disabled={loading || !areParamsValid()}
                className="inline-flex items-center justify-center rounded-xl bg-white px-6 py-3 font-semibold text-slate-900 transition hover:scale-[1.02] disabled:opacity-60"
              >
                {loading ? 'Generando...' : 'Generar Configuración'}
              </button>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}