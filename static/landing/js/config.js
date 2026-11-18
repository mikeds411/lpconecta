/* =========================================================
   CONFIGURAÇÃO DOS WHATSAPPS
   Troque aqui os números de cada clínica (formato: 55 + DDD + número,
   somente dígitos). Não é preciso mexer no HTML.
   Enquanto uma clínica estiver sem número próprio, vale o número geral.
   ========================================================= */
window.CONECTA_CONFIG = {
  // Número geral do projeto (rodapé e botão flutuante)
  whatsappGeral: "5561999999999",

  // Número de cada clínica. Deixe "" para usar o número geral.
  clinicas: {
    medicina:     { nome: "Medicina",              whatsapp: "" },
    enfermagem:   { nome: "Enfermagem",            whatsapp: "" },
    nutricao:     { nome: "Nutrição",              whatsapp: "" },
    odontologia:  { nome: "Odontologia",           whatsapp: "" },
    fisioterapia: { nome: "Fisioterapia",          whatsapp: "" },
    psicologia:   { nome: "Psicologia",            whatsapp: "" },
    estetica:     { nome: "Estética",              whatsapp: "" },
    veterinaria:  { nome: "Medicina Veterinária",  whatsapp: "" }
  }
};
