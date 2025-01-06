CREATE TABLE case_in_vendita (
    catastale VARCHAR(50) PRIMARY KEY,
    indirizzo VARCHAR(255) NOT NULL,
    numero_civico INT NOT NULL,
    piano INT NOT NULL,
    metri FLOAT NOT NULL,
    vani INT NOT NULL,
    prezzo INT NOT NULL,
    stato ENUM('LIBERO', 'OCCUPATO') NOT NULL,
    filiale_proponente VARCHAR(50) NOT NULL,
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva)
);

CREATE TABLE case_in_affitto (
    catastale VARCHAR(50) PRIMARY KEY,
    indirizzo VARCHAR(255) NOT NULL,
    civico INT NOT NULL,
    tipo_affitto ENUM('PARZIALE', 'TOTALE') NOT NULL,
    bagno_personale BOOLEAN NOT NULL,
    prezzo_mensile INT NOT NULL,
    filiale_proponente VARCHAR(50) NOT NULL,
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva)
);

CREATE TABLE filiali (
    partita_iva VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    indirizzo_sede VARCHAR(255) NOT NULL,
    civico INT NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

CREATE TABLE vendite_casa (
    catastale VARCHAR(50) NOT NULL,
    data_vendita DATE NOT NULL,
    filiale_proponente VARCHAR(50) NOT NULL,
    filiale_venditrice VARCHAR(50) NOT NULL,
    prezzo_vendita INT NOT NULL,
    PRIMARY KEY (catastale, data_vendita),
    FOREIGN KEY (catastale) REFERENCES case_in_vendita(catastale),
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva),
    FOREIGN KEY (filiale_venditrice) REFERENCES filiali(partita_iva)
);

CREATE TABLE affitti_casa (
    catastale VARCHAR(50) NOT NULL,
    data_affitto DATE NOT NULL,
    filiale_proponente VARCHAR(50) NOT NULL,
    filiale_venditrice VARCHAR(50) NOT NULL,
    prezzo_affitto INT NOT NULL,
    durata_contratto INT NOT NULL,
    PRIMARY KEY (catastale, data_affitto),
    FOREIGN KEY (catastale) REFERENCES case_in_affitto(catastale),
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva),
    FOREIGN KEY (filiale_venditrice) REFERENCES filiali(partita_iva)
);
