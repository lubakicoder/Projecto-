const ADMINS = [];
const MEDICOS_DB = [];
const API = {
    auth: "/api/auth",
    atendimento: "/api/atendimentos"
};


let DB = {
    atendimentos:[]
};

async function carregarAtendimentos(){
    try{
        const res = await fetch(API.atendimento);
        const data = await res.json();
        DB.atendimentos = data.atendimentos || [];
    }catch(err){
        console.error(err);
        DB.atendimentos = [];
    }
}

const SINTOMAS=['Febre','Dor de cabeça','Tosse','Coriza','Dor no peito','Falta de ar','Náusea','Vômito','Dor abdominal','Tontura','Cansaço','Dor nas costas'];
let session=null, tab=0, selSint=[], editId=null;

function togglePac(mode){
    document.getElementById("pacLogin").style.display = mode === "login" ? "block" : "none";
    document.getElementById("pacRegister").style.display = mode === "register" ? "block" : "none";

    document.getElementById("tabLogin").classList.toggle("active", mode === "login");
    document.getElementById("tabRegister").classList.toggle("active", mode === "register");
}

function goScreen(id){
          document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
          document.getElementById(id).classList.add('active');
          ['errAdm','errMed','errPac'].forEach(e=>{const el=document.getElementById(e);if(el)el.classList.add('hidden');});
}
function goLogin(r){goScreen(r==='admin'?'scrAdmin':r==='medico'?'scrMedico':'scrPaciente');}
function maskCPF(el){let v=el.value.replace(/\D/g,'');if(v.length>9)v=v.replace(/^(\d{3})(\d{3})(\d{3})(\d{0,2}).*/,'$1.$2.$3-$4');else if(v.length>6)v=v.replace(/^(\d{3})(\d{3})(\d{0,3}).*/,'$1.$2.$3');else if(v.length>3)v=v.replace(/^(\d{3})(\d{0,3}).*/,'$1.$2');el.value=v;}

function showErr(box,msg,msgId){document.getElementById(box).classList.remove('hidden');if(msgId)document.getElementById(msgId).textContent=msg;}

async function loginAdmin(){
    const username =
        document.getElementById("admUser").value.trim();
    const password =
        document.getElementById("admPass").value;
    const res = await fetch(
        `${API.auth}/admin/login`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                username,
                password
            })
        }
    );
    const data = await res.json();
    if(data.success){
        session = {
            role:"admin",
            nome:data.admin.nome
        };
        openDash();
    }else{
        alert(data.message);
    }
}

async function loginMedico(){
    const crm =
        document.getElementById("medCRM").value.trim();
    const senha =
        document.getElementById("medPass").value;
    const res = await fetch(
        `${API.auth}/medico/login`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                crm,
                senha
            })
        }
    );
    const data = await res.json();
    if(data.success){
        session = {
            role:"medico",
            nome:data.medico.nome,
            crm:data.medico.crm,
            espec:data.medico.especialidade
        };
        openDash();
    }else{
        alert(data.message);
    }
}

async function registerPaciente(){
    const res = await fetch("/api/auth/paciente/register", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            nome: document.getElementById("rNome").value,
            bi: document.getElementById("rBI").value,
            data_nascimento: document.getElementById("rData").value,
            telefone: document.getElementById("rTel").value,
            email: document.getElementById("rEmail").value,
            senha: document.getElementById("rSenha").value
        })
    });

    const data = await res.json();

    if(data.success){
        alert("Conta criada com sucesso!");
        togglePac("login");
    } else {
        alert(data.message);
    }
}

async function loginPaciente(){

    const email =
        document.getElementById("pacEmail").value.trim();

    const senha =
        document.getElementById("pacSenha").value.trim();

    const res = await fetch(
        `${API.auth}/paciente/login`,
        {
            method: "POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                email,
                senha
            })
        }
    );

    const data = await res.json();

    if(data.success){

        session = {
            role: "paciente",
            nome: data.paciente.nome,
            bi: data.paciente.bi,
            email: data.paciente.email,
        };

        openDash();

    }else{

        alert(data.message);

    }
}

async function openDash(){
    tab = 0;
    selSint = [];
    editId = null;
    document
        .querySelectorAll(".screen")
        .forEach(s => s.classList.remove("active"));
    document
        .getElementById("mainWrap")
        .classList
        .remove("hidden");
    const bmap = {
        admin:['tb-admin','ADMIN'],
        medico:['tb-medico','MÉDICO'],
        paciente:['tb-paciente','PACIENTE']
    };
    const [bc, bl] = bmap[session.role];
    const badge =
        document.getElementById("tBadge");
    badge.textContent = bl;
    badge.className = "t-badge " + bc;
    document
        .getElementById("tUser")
        .textContent = session.nome;
    document
        .getElementById("tExtra")
        .innerHTML =
            session.crm
                ? `<span class="crm-tag">${session.crm}</span>`
                : "";
    await carregarAtendimentos();
    render();
}

async function logout(){
    await fetch(
        `${API.auth}/logout`,
        {
            method:"POST"
        }
    );
    session = null;
    location.reload();
}

function setTab(t){tab=t;editId=null;render();}
function render(){
          const c=document.getElementById('mainContent');
          c.innerHTML='';c.classList.remove('anim');void c.offsetWidth;c.classList.add('anim');
          if(session.role==='paciente')renderPaciente(c);
          else if(session.role==='medico')renderMedico(c);
          else renderAdmin(c);
}


function renderPaciente(c){
          const meu=DB.atendimentos.find(a=>a.bi===session.bi);
          c.innerHTML=`
            <div class="nav-tabs">
                <button class="ntab ${tab===0?'active':''}" onclick="setTab(0)"><i class="ti ti-edit"></i> Registrar Sintomas</button>
                    <button class="ntab ${tab===1?'active':''}" onclick="setTab(1)"><i class="ti ti-activity"></i> Meu Atendimento</button>
                      </div>
                        ${tab===0?formPac():statusPac(meu)}`;
          document.querySelectorAll('.stag').forEach(el=>{
                      el.onclick=()=>{const s=el.dataset.s;selSint.includes(s)?selSint=selSint.filter(x=>x!==s):selSint.push(s);el.classList.toggle('sel',selSint.includes(s));};
                    });
}

function formPac(){
return `<div class="card">

<div class="card-title">
<i class="ti ti-clipboard-list"></i>
Formulário de sintomas
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">

<div class="fgroup">
<label class="flabel">Paciente</label>
<input class="finput" disabled value="${session.nome}">
</div>

<div class="fgroup">
<label class="flabel">BI</label>
<input class="finput" disabled value="${session.bi}">
</div>

</div>

<div class="fgroup">
<label class="flabel">Selecione os sintomas</label>

<div class="stag-grid">

${SINTOMAS.map(s=>`
<div class="stag${selSint.includes(s)?' sel':''}" data-s="${s}">
<i class="ti ti-circle-dotted"></i>
${s}
</div>
`).join('')}

</div>

</div>

<div class="fgroup">

<label class="flabel">
Intensidade dos sintomas —
<strong id="intLbl" style="color:var(--accent2)">5</strong>/10
</label>

<input
type="range"
id="pInt"
min="1"
max="10"
value="5"
style="width:100%"
oninput="document.getElementById('intLbl').textContent=this.value">

</div>

<div class="fgroup">
<label class="flabel">Observações</label>

<textarea
class="ftextarea"
id="pObs"
placeholder="Quando começaram os sintomas?">
</textarea>

</div>

<button
class="btn-main"
onclick="enviarTriagem()"
style="width:auto;padding:10px 28px">

<i class="ti ti-send"></i>
Enviar para triagem

</button>

</div>`;
}


function statusPac(meu){
          if(!meu)return`<div class="card" style="text-align:center;padding:3rem"><i class="ti ti-clipboard-off" style="font-size:40px;color:var(--text3)"></i><p style="margin-top:1rem;color:var(--text2)">Nenhum atendimento registrado ainda.</p><p style="color:var(--text3);font-size:13px;margin-top:4px">Registre seus sintomas na aba anterior.</p></div>`;
          const dbox=meu.diag?`<div class="diag-box diag-${meu.prioridade}"><strong><i class="ti ti-notes-medical"></i> Pré-diagnóstico médico</strong><p>${meu.diag}</p></div>`:`<div style="margin-top:1rem;padding:1rem;background:var(--bg3);border-radius:var(--r-sm);color:var(--text2);font-size:13px;text-align:center"><i class="ti ti-clock"></i> Aguardando avaliação médica...</div>`;
          return`<div class="card">
            <div class="row" style="margin-bottom:1.25rem;gap:14px">
                <div class="avatar av-amber" style="background:rgba(245,158,11,0.15);color:#fbbf24"><i class="ti ti-user"></i></div>
                    <div class="flex1"><p style="font-weight:600;font-size:15px">${meu.paciente}</p><p style="color:var(--text2);font-size:13px">${meu.data_nascimento}  · BI ${meu.bi}</p></div>
                        <span class="pill p-${meu.status}">${meu.status.replace('-',' ')}</span>
                          </div>
                            <p style="font-size:12px;color:var(--text3);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">Sintomas informados</p>
                              <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1rem">${meu.sintomas.map(s=>`<span class="pill p-moderado">${s}</span>`).join('')}</div>
                                <p style="font-size:13px;color:var(--text2)"><i class="ti ti-activity"></i> Intensidade: <strong style="color:var(--text)">${meu.intensidade}/10</strong> &nbsp;·&nbsp; ${meu.observacao}</p>
                                  ${dbox}
                                  </div>`;}

async function enviarTriagem(){

    const intensidade =
        parseInt(document.getElementById("pInt").value);

    const observacao =
        document.getElementById("pObs").value.trim();

    if(selSint.length === 0){
        alert("Selecione ao menos um sintoma");
        return;
    }

    const prioridade =
        intensidade >= 8 ? "urgente"
        : intensidade >= 5 ? "moderado"
        : "leve";

    const res = await fetch(API.atendimento,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            sintomas: selSint,
            intensidade,
            prioridade,
            observacao
        })
    });

    const data = await res.json();

    if(data.success){
        await carregarAtendimentos();
        tab = 1;
        render();
    }else{
        alert(data.message);
    }
}            


function renderMedico(c){
          const pend=DB.atendimentos.filter(a=>a.status!=='concluido');
          const conc=DB.atendimentos.filter(a=>a.status==='concluido');
          c.innerHTML=`
            <div class="nav-tabs">
                <button class="ntab ${tab===0?'active':''}" onclick="setTab(0)"><i class="ti ti-list-check"></i> Fila de Triagem <span style="background:rgba(245,158,11,0.15);color:#fcd34d;border-radius:99px;font-size:10px;padding:1px 7px;margin-left:4px;border:1px solid rgba(245,158,11,0.2)">${pend.length}</span></button>
                    <button class="ntab ${tab===1?'active':''}" onclick="setTab(1)"><i class="ti ti-circle-check"></i> Concluídos</button>
                        <button class="ntab ${tab===2?'active':''}" onclick="setTab(2)"><i class="ti ti-user-circle"></i> Meu Perfil</button>
                          </div>
                            ${tab===0?filaMed(pend):tab===1?concMed(conc):perfilMed()}
                              ${editId?evalCard():''}`;
}
function filaMed(lista){
          if(!lista.length)return`<div class="card" style="text-align:center;padding:3rem"><i class="ti ti-circle-check" style="font-size:40px;color:#10b981"></i><p style="margin-top:1rem;color:var(--text2)">Nenhum atendimento pendente.</p></div>`;
          const sorted=[...lista].sort((a,b)=>({urgente:0,moderado:1,leve:2}[a.prioridade]||2)-({urgente:0,moderado:1,leve:2}[b.prioridade]||2));
          return`<div class="card tbl-wrap"><table>
              <thead><tr><th>Paciente</th><th>BI</th><th>Sintomas</th><th>Intensidade</th><th>Prioridade</th><th>Status</th><th>Ação</th></tr></thead>
                  <tbody>${sorted.map(a=>`<tr>
                        <td><strong>${a.paciente}</strong></td>
                              <td style="color:var(--text2);font-size:12px">${a.bi ||'-'}</td>
                                    <td style="font-size:12px;color:var(--text2)">${a.sintomas.slice(0,2).join(', ')}${a.sintomas.length>2?` <span style="color:var(--text3)">+${a.sintomas.length-2}</span>`:''}</td>
                                          <td><span style="font-weight:600;color:${a.intensidade>=8?'#f87171':a.intensidade>=5?'#fbbf24':'#6ee7b7'}">${a.intensidade}/10</span></td>
                                               <td><span class="pill p-${a.prioridade}">${a.prioridade}</span></td>
                                             <td><span class="pill p-${a.status}">${a.status.replace('-',' ')}</span></td>
                                                   <td><button class="btn-sm ok" onclick="abrirEval(${a.id})"><i class="ti ti-stethoscope"></i> Avaliar</button></td>
                                               </tr>`).join('')}</tbody>
                                         </table></div>`;}
function concMed(lista){
          if(!lista.length)return`<div class="card" style="text-align:center;padding:3rem"><p style="color:var(--text2)">Nenhum atendimento concluído ainda.</p></div>`;
          return`<div class="card tbl-wrap"><table>
              <thead><tr><th>Paciente</th><th>Diagnóstico</th><th>Prioridade</th><th>Status</th></tr></thead>
                  <tbody>${lista.map(a=>`<tr>
                        <td>${a.paciente}</td>
                              <td style="font-size:12px;color:var(--text2);max-width:200px">${a.diag||'-'}</td>
                                    <td><span class="pill p-${a.prioridade}">${a.prioridade}</span></td>
                                          <td><span class="pill p-concluido">concluído</span></td>
                                             </tr>`).join('')}</tbody>
                                               </table></div>`;}

function perfilMed(){return`<div class="card" style="max-width:420px">
  <div class="row" style="gap:14px;margin-bottom:1.5rem">
      <div class="avatar av-green"><i class="ti ti-stethoscope"></i></div>
          <div><p style="font-weight:600;font-size:16px">${session.nome}</p><p style="color:var(--text2);font-size:13px">${session.espec}</p></div>
            </div>
              <table style="width:100%;font-size:13px">
                  <tr><td style="color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border)">CRM</td><td style="text-align:right;padding:8px 0;border-bottom:1px solid var(--border)"><span class="crm-tag">${session.crm}</span></td></tr>
                      <tr><td style="color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border)">Especialidade</td><td style="text-align:right;padding:8px 0;border-bottom:1px solid var(--border);color:var(--text2)">${session.espec}</td></tr>
                          <tr><td style="color:var(--text3);padding:8px 0">Atendimentos concluídos</td><td style="text-align:right;padding:8px 0;color:#6ee7b7;font-weight:600">${DB.atendimentos.filter(a=>a.status==='concluido').length}</td></tr>
                            </table>
                            </div>`;}

function abrirEval(id){
    editId = id;
    render();
}

function evalCard(){
          const a=DB.atendimentos.find(x=>x.id===editId);
          if(!a)return'';
          return`<div class="eval-card card">
            <div class="card-title"><i class="ti ti-clipboard-text"></i> Avaliação — ${a.paciente}</div>
              <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:1.25rem">
                  <div style="background:var(--bg3);border-radius:var(--r-sm);padding:10px 14px"><div style="font-size:11px;color:var(--text3);margin-bottom:2px">Nascido</div><div style="font-size:13px;color:var(--text2)">${a.data_nascimento}</div></div>
                      <div style="background:var(--bg3);border-radius:var(--r-sm);padding:10px 14px"><div style="font-size:11px;color:var(--text3);margin-bottom:2px">INTENSIDADE</div><div style="font-size:13px;color:var(--text2)">${a.intensidade}/10</div></div>
                          <div style="background:var(--bg3);border-radius:var(--r-sm);padding:10px 14px"><div style="font-size:11px;color:var(--text3);margin-bottom:2px">PRIORIDADE</div><div style="font-size:13px;color:var(--text2)">${a.prioridade}</div></div>
                            </div>
                              <div class="fgroup"><label class="flabel">Sintomas informados</label><div style="display:flex;flex-wrap:wrap;gap:6px">${a.sintomas.map(s=>`<span class="pill p-moderado">${s}</span>`).join('')}</div></div>
                                <div class="fgroup"><label class="flabel">Observações do paciente</label><div style="background:var(--bg3);border-radius:var(--r-sm);padding:10px 14px;font-size:13px;color:var(--text2)">${a.observacao}</div></div>
                                  <div class="fgroup"><label class="flabel">Diagnóstico / Conduta</label><textarea class="ftextarea" id="diagText" placeholder="Descreva o diagnóstico e conduta recomendada...">${a.diag}</textarea></div>
                                    <div class="row" style="gap:10px">
                                        <button class="btn-main green" onclick="salvarDiag()" style="width:auto;padding:10px 24px"><i class="ti ti-check"></i> Salvar e Concluir</button>
                                           <button class="btn-back" onclick="editId=null;render()" style="width:auto;margin:0"><i class="ti ti-x"></i> Cancelar</button>
                                             </div>
                                             </div>`;}

async function salvarDiag(){
    const diag =
        document
            .getElementById("diagText")
            .value
            .trim();
    if(!diag){
        alert("Escreva o diagnóstico");
        return;
    }
    const res = await fetch(
        `${API.atendimento}/${editId}`,
        {
            method:"PUT",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                diagnostico:diag,
                status:"concluido"
            })
        }
    );
    const data = await res.json();
    if(data.success){
        editId = null;
        await carregarAtendimentos();
        tab = 1;
        render();
    }else{
        alert(data.message);
    }
}




function dashAdmin(total,pend,conc){
          return`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin-bottom:24px">
              <div class="card" style="margin:0"><div style="font-size:12px;color:var(--text3);margin-bottom:8px">TOTAL</div><div style="font-size:32px;font-weight:700">${total}</div></div>
                  <div class="card" style="margin:0"><div style="font-size:12px;color:var(--text3);margin-bottom:8px">PENDENTES</div><div style="font-size:32px;font-weight:700;color:var(--amber)">${pend}</div></div>
                      <div class="card" style="margin:0"><div style="font-size:12px;color:var(--text3);margin-bottom:8px">CONCLUÍDOS</div><div style="font-size:32px;font-weight:700;color:var(--green)">${conc}</div></div>
                        </div>`;
}
function listaAdmin(){
  return `
  <div class="card tbl-wrap">
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Paciente</th>
          <th>BI</th>
          <th>Prioridade</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        ${DB.atendimentos.map(a => `
          <tr>
            <td>${a.id}</td>
            <td>${a.paciente}</td>
            <td>${a.bi || '-'}</td>
            <td><span class="pill p-${a.prioridade}">${a.prioridade}</span></td>
            <td><span class="pill p-${a.status}">${a.status}</span></td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  </div>`;
}

async function criarMedico(){
  const crm = document.getElementById("admMedCRM").value;
  const nome = document.getElementById("admMedNome").value;
  const espec = document.getElementById("admMedEsp").value;
  const senha = document.getElementById("admMedPass").value;

  const res = await fetch(`${API.auth}/medico/register`, {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({ crm, nome, espec, senha })
  });

  const data = await res.json();

  if(data.success){
    alert("Médico cadastrado com sucesso!");
  }else{
    alert(data.message);
  }
}

function renderMedicosAdmin(){
  return `
    <div class="card">
      <div class="card-title">Cadastrar Médico</div>

      <div class="fgroup">
        <label class="flabel">CRM</label>
        <input class="finput" id="admMedCRM" placeholder="CRM-12345">
      </div>

      <div class="fgroup">
        <label class="flabel">Nome</label>
        <input class="finput" id="admMedNome">
      </div>

      <div class="fgroup">
        <div class="fgroup"><label class="flabel">Especialidade</label>
        <select class="fselect" id="admMedEsp" >
        <option value="">Selecione...</option>
        <option>Clínica Geral</option><option>Cardiologia</option><option>Pediatria</option>
        <option>Neurologia</option><option>Ortopedia</option><option>Ginecologia</option>
        </select>
       </div>
      </div>

      <div class="fgroup">
        <label class="flabel">Senha</label>
        <input class="finput" id="admMedPass" type="password">
      </div>

      <button class="btn-main green" onclick="criarMedico()">
        Cadastrar Médico
      </button>
    </div>
  `;
}

function renderAdmin(c){
  const total = DB.atendimentos.length;
  const pend = DB.atendimentos.filter(a=>a.status!=='concluido').length;
  const conc = DB.atendimentos.filter(a=>a.status==='concluido').length;

  c.innerHTML = `
    <div class="nav-tabs">
      <button class="ntab ${tab===0?'active':''}" onclick="setTab(0)">
        <i class="ti ti-dashboard"></i> Dashboard
      </button>

      <button class="ntab ${tab===1?'active':''}" onclick="setTab(1)">
        <i class="ti ti-users"></i> Atendimentos
      </button>

      <button class="ntab ${tab===2?'active':''}" onclick="setTab(2)">
        <i class="ti ti-stethoscope"></i> Médicos
      </button>
    </div>

    ${
      tab===0 ? dashAdmin(total,pend,conc)
      : tab===1 ? listaAdmin()
      : tab===2 ? renderMedicosAdmin()
      : ""
    }
  `;
}
