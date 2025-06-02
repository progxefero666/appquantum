# src/models/element.py

from typing import Optional, Dict, Any

class Element:
    """
    Representa un elemento de la tabla periódica, mapeado a la tabla 'elements' en SQLite.
    """
    def __init__(self,
                 atomic_number: int,
                 name: str,
                 symbol: str,
                 mass_number: Optional[int] = None,
                 atomic_weight: Optional[float] = None,
                 density: Optional[float] = None,
                 melting_point: Optional[float] = None,
                 boiling_point: Optional[float] = None,
                 group: Optional[int] = None,  # Mapea a 'egroup' en la BBDD
                 period: Optional[int] = None, # Mapea a 'periodo' en la BBDD
                 block: Optional[str] = None,
                 category: Optional[str] = None,
                 application: Optional[str] = None,
                 econfig: Optional[str] = None):

        self.atomic_number: int = atomic_number
        self.mass_number: Optional[int] = mass_number
        self.name: str = name
        self.symbol: str = symbol
        self.atomic_weight: Optional[float] = atomic_weight
        self.density: Optional[float] = density
        self.melting_point: Optional[float] = melting_point
        self.boiling_point: Optional[float] = boiling_point
        self.group: Optional[int] = group
        self.period: Optional[int] = period
        self.block: Optional[str] = block
        self.category: Optional[str] = category
        self.application: Optional[str] = application
        self.econfig: Optional[str] = econfig

    def __repr__(self) -> str:
        """
        Representación oficial del objeto, útil para debugging.
        Debería ser posible recrear el objeto con eval(repr(objeto)).
        """
        return (f"Element(atomic_number={self.atomic_number!r}, name={self.name!r}, symbol={self.symbol!r}, "
                f"mass_number={self.mass_number!r}, atomic_weight={self.atomic_weight!r}, "
                f"density={self.density!r}, melting_point={self.melting_point!r}, "
                f"boiling_point={self.boiling_point!r}, group={self.group!r}, "
                f"period={self.period!r}, block={self.block!r}, category={self.category!r}, "
                f"application={self.application!r}, econfig={self.econfig!r})")

    def __str__(self) -> str:
        """
        Representación legible del objeto.
        """
        return f"{self.name} ({self.symbol}) - Atomic #: {self.atomic_number}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la instancia del Elemento a un diccionario.
        Útil para serializar o para insertar en BBDD donde los nombres de columna coinciden.
        """
        return {
            "atomicnumber": self.atomic_number, # Coincide con nombre de columna BBDD
            "massnumber": self.mass_number,     # Coincide con nombre de columna BBDD
            "name": self.name,
            "symbol": self.symbol,
            "atomicweight": self.atomic_weight, # Coincide con nombre de columna BBDD
            "density": self.density,
            "meltingpoint": self.melting_point, # Coincide con nombre de columna BBDD
            "boilingpoint": self.boiling_point, # Coincide con nombre de columna BBDD
            "egroup": self.group,         # Mapea 'group' del objeto a 'egroup' de BBDD
            "periodo": self.period,       # Mapea 'period' del objeto a 'periodo' de BBDD
            "block": self.block,
            "category": self.category,
            "application": self.application,
            "econfig": self.econfig
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Element':
        """
        Crea una instancia de Element a partir de un diccionario.
        Asume que las claves del diccionario coinciden con los parámetros del constructor
        o con los nombres de las columnas de la BBDD (con el mapeo apropiado).
        """
        return cls(
            atomic_number=data.get('atomicnumber', data.get('atomic_number')), # 'atomicnumber' es el de la BBDD
            mass_number=data.get('massnumber', data.get('mass_number')),
            name=data.get('name'),
            symbol=data.get('symbol'),
            atomic_weight=data.get('atomicweight', data.get('atomic_weight')),
            density=data.get('density'),
            melting_point=data.get('meltingpoint', data.get('melting_point')),
            boiling_point=data.get('boilingpoint', data.get('boiling_point')),
            group=data.get('egroup', data.get('group')), # Prioriza 'egroup' (BBDD) o 'group' (JSON)
            period=data.get('periodo', data.get('period')), # Prioriza 'periodo' (BBDD) o 'period' (JSON)
            block=data.get('block'),
            category=data.get('category'),
            application=data.get('application'),
            econfig=data.get('econfig')
        )