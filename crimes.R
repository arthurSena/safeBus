path = "/home/tales/development/Git/hackaton/Espelho_CVP_Campina_Grande_2014.csv"
crimes <- read.table(file = path, sep=";", header=T)

roubos_descartados = c("Roubo a Est Bancario", "Roubo a Lotérica e Corresp. Bancário", "Roubo a Igreja", "Roubo de Carga", "Roubo em Veículo", "Roubo em Hotéis e Similares", "Roubo de Carro", "Roubo a Posto de Combustível", "Roubo a Residência")

roubos_considerados = crimes[!is.element(crimes$Natureza, roubos_descartados),]
row.names(roubos_considerados) = NULL

write.csv(roubos_considerados, file = "/home/tales/development/Git/hackaton/crimes_considerados.csv", row.names = FALSE)