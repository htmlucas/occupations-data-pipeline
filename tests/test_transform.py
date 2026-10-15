
import unittest

import pandas as pd

from src.transform import transform_occupations


class TestTransformOccupations(unittest.TestCase):

    def test_aceita_dataframe_valido(self):
        df = pd.DataFrame({
            "CODIGO": ["12345", "54321"],
            "TITULO": [
                "Analista de dados",
                "Desenvolvedor de software"
            ]
        })

        resultado = transform_occupations(df)

        self.assertEqual(len(resultado), 2)
        self.assertEqual(
            resultado["CODIGO"].tolist(),
            ["12345", "54321"]
        )

    def test_rejeita_coluna_obrigatoria_ausente(self):
        df = pd.DataFrame({
            "CODIGO": ["12345"]
        })

        with self.assertRaisesRegex(
            ValueError, "Colunas obrigatórias ausentes"
        ):
            transform_occupations(df)

    def test_rejeita_codigo_duplicado(self):
        df = pd.DataFrame({
            "CODIGO": ["12345", "12345"],
            "TITULO": ["Analista", "Programador"]
        })

        with self.assertRaisesRegex(
            ValueError, "Codigo não pode ser nulo"
        ):
            transform_occupations(df)

    def test_rejeita_titulo_nulo(self):
        df = pd.DataFrame({
            "CODIGO": ["12345"],
            "TITULO": [None]
        })

        with self.assertRaisesRegex(
            ValueError, "Titulo não pode estar vazio"
        ):
            transform_occupations(df)

    def test_rejeita_dataframe_vazio(self):
        df = pd.DataFrame(columns=["CODIGO", "TITULO"])

        with self.assertRaisesRegex(
            ValueError, "Quantidade de registros não pode ser zero"
        ):
            transform_occupations(df)


if __name__ == "__main__":
    unittest.main()
