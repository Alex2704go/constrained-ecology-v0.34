# cross_mapping_engine.py
"""
CROSS-MAPPING & ST_SURROGATE NUMERICAL ENGINE
=============================================
Direct implementation of the physically and topologically anchored cross-mapping table.
Calculates the ST_surrogate metric from NMR observables and graph structures,
and maps them to physical regimes, flask observations, microscopic models, and validation actions.
"""

from typing import Dict, Any
from src.ontology_layers import Layer0MolecularGraph

class STSurrogateCalculator:
    """
    ST_surrogate calculator.
    Calculates the surrogate adaptation metric from physical NMR variables:
    - mean_proton_deviation (solvent transfer sensitivity)
    - temperature (thermal forcing parameter)
    - topology_cost (structural complexity resistance)
    - rigidity_index (inherent molecular graph resistance)
    - anomaly effects (Nitriles protect/stabilize; Halogens destabilize/deconfine)
    """
    @staticmethod
    def calculate_surrogate(
        mean_proton_deviation: float,
        temperature_K: float,
        topology_cost: float,
        rigidity_index: float,
        has_coupled_synergy: bool,
        is_unstructured: bool = False
    ) -> float:
        """
        Mathematical model anchoring the ML surrogate to physical observables.
        Returns a value from 0.0 to 1.0 representing the stiffness/stability state.
        """
        if is_unstructured:
            # Random noise fields are highly deconfined and unorganized
            return 0.45
            
        # Normalize variables
        # Base proton deviation effect (max around 2.0 ppm)
        p_effect = min(2.0, mean_proton_deviation) / 2.0
        
        # Temperature forcing: normalized against room temp (298K)
        # Higher temperatures increase thermal forcing (destabilizing the scaffold)
        t_effect = max(0.5, min(2.5, temperature_K / 298.0))
        
        # Topology cost: represents barrier resistance. High cost means system is driven hard
        cost_effect = min(3.0, (topology_cost + 1.0) / 15.0)
        
        # Rigidity index: high rigidity (e.g. Nitrile = 6.0) suppresses ST_surrogate,
        # keeping it in the Latent/Protected zones. Low rigidity (flexible or halogenated = 0.8) elevates it.
        r_factor = max(0.5, rigidity_index)
        
        # Compute surrogate value
        st_base = (p_effect * t_effect * (cost_effect ** 0.5)) / r_factor
        
        # Apply coupled anomaly correction (Boron-Halogen synergy index)
        if has_coupled_synergy:
            # Boron-Halogen coupling suppresses exploratory liberation, keeping it in localized protected corridors
            st_base *= 0.7
            
        # Hard limit to realistic physical scale
        return max(0.01, min(0.99, float(st_base)))


class CrossMappingClassifier:
    """
    Cross-Mapping Classifier.
    Translates the numerical ST_surrogate value into concrete, physically interpretable
    concepts and laboratory guidelines in Russian (as requested by Alexei).
    """
    @staticmethod
    def classify(st_surrogate: float) -> Dict[str, Any]:
        if st_surrogate < 0.10:
            return {
                "regime_id": "LATENT_JAMMED",
                "color": "🔴 RED",
                "name": "LATENT JAMMED (Скрытая блокировка)",
                "conversion_metric": "Конверсия < 5% за часы",
                "in_flask": "Реакция не идёт или идёт с длинным индукционным периодом. Добавление избытка реагента не меняет картину. Система 'мёртвая', но не смолится (экзотерма отсутствует).",
                "microscopic_candidate": "Плотные агрегаты (димеры, тетрамеры), активный центр пространственно или электронно недоступен. Trapping-агенты доминируют (вода, сильное хелатирование). Гигантское насыщение транспорта (transmissibility = 0).",
                "validation_methods": "DOSY ЯМР (низкий коэффициент диффузии D), осмометрия, рентгеноструктурный анализ (РША) кристаллов реагента; титрование Карла Фишера, ЯМР-титрование субстратом; калориметрия (нет тепловыделения), измерение вязкости.",
                "example": "BuLi в эфире при -78°C.",
                "framework_insight": "Ищи плотные агрегаты BuLi, запертые эфирной оболочкой. Нагрей реакционную смесь или добавь TMEDA — агрегаты раскроются, и система перейдёт в режим Protected."
            }
        elif 0.10 <= st_surrogate < 0.18:
            return {
                "regime_id": "PROTECTED",
                "color": "🟡 YELLOW",
                "name": "PROTECTED (Защищённый стабильный)",
                "conversion_metric": "Конверсия 50–80% за часы",
                "in_flask": "Реакция идёт медленно, но стабильно, выход продукта воспроизводимый. Слабая чувствительность к температуре (колебания в пределах ±10°C не меняют выход радикально). Избыток реагента не вызывает смоления.",
                "microscopic_candidate": "Один доминирующий спейсинг (speciation state) или узкое термодинамическое равновесие двух близких форм. Активационный барьер высокий, но предэкспоненциальный множитель (pre-exponential factor) маленький. Каркас (scaffold) стабилен, принуждение (forcing) слабое.",
                "validation_methods": "NMR-speciation (один чистый набор сигналов), кинетические кривые строго первого порядка; график Аррениуса (определение Ea и ln A), кинетика в интервале температур; титрование реагентом с мониторингом чистоты (ВЭЖХ, ГХ).",
                "example": "K2CO3 в ацетоне при 40°C.",
                "framework_insight": "Один доминирующий вид реагента на поверхности карбоната. Не перегревай смесь выше 50°C, иначе сорвёшься в Boundary Zone."
            }
        elif 0.18 <= st_surrogate <= 0.24:
            return {
                "regime_id": "PROTECTED_COHERENT",
                "color": "🟢 GREEN",
                "name": "PROTECTED COHERENT (Согласованный защищённый)",
                "conversion_metric": "Выход > 80%, моно/бис > 10:1",
                "in_flask": "Хороший выход, высокая селективность. Проявляется чувствительность к следам влаги (даже 0.1% H2O меняет выход на 10–20%). Узкое температурное окно (колебания ±5°C — разница между успехом и провалом реакции).",
                "microscopic_candidate": "Динамическое равновесие между двумя активными формами (speciation states). Вода выступает в роли медиатора (mediator), сдвигая равновесие. Температурный фактор (temp_factor) эффективно переключает доминирующий активный вид.",
                "validation_methods": "ЯМР-спектроскопия — два набора сигналов в быстром обмене, VT-NMR (динамический ЯМР при разных температурах); титрование водой с контролем кинетики; VT-кинетика, DSC (калориметрия для фиксации тепловых эффектов при нагреве).",
                "example": "BuLi в ТГФ при 0°C, DIEA в MeCN при 25°C.",
                "framework_insight": "Ищи два активных компонента в равновесии. Вода, температура, избыток реагента — всё сдвигает это равновесие. VT-NMR — твой главный калибровочный инструмент."
            }
        elif 0.24 < st_surrogate <= 0.33:
            return {
                "regime_id": "BOUNDARY_ZONE",
                "color": "⚠️ ORANGE",
                "name": "BOUNDARY ZONE (Пограничная зона перехода)",
                "conversion_metric": "Выход нестабилен (от 20% до 80%)",
                "in_flask": "Резкая зависимость выхода от порядка добавления реагентов. Гиперчувствительность к перемешиванию (с мешалкой — 90%, без — 40%, и это не из-за диффузии!). Воспроизводимость результатов отвратительная (у разных химиков разные выходы).",
                "microscopic_candidate": "Переход через порог деконфайнмента (deconfinement threshold): малейшее внешнее возмущение переключает доминирующий вид спейсинга. Локальные градиенты концентрации мгновенно перестраивают молекулярные ансамбли. Система на границе фазового перехода.",
                "validation_methods": "Кинетика при разном порядке смешения,stopped-flow спектроскопия; сравнение выходов при разной скорости вращения мешалки + мониторинг in situ (ReactIR); детальная статистика идентичных запусков для оценки дисперсии.",
                "example": "ДМФА + K2CO3 при 40°C.",
                "framework_insight": "Ты сидишь прямо на границе переключения молекулярных фаз. Любой минимальный фактор убьёт селективность. Контролируй всё: влажность, скорость перемешивания, температуру до ±1°C. Или уходи в Protected-режим (меняй растворитель на ацетон)."
            }
        else: # st_surrogate > 0.33
            return {
                "regime_id": "RUNAWAY",
                "color": "💥 BLACK",
                "name": "RUNAWAY TRANSMISSIVE (Неуправляемый прорыв)",
                "conversion_metric": "Выход < 30%, остальное — гудрон",
                "in_flask": "Быстрое смоление реакционной массы, обилие побочных продуктов. Интенсивное неконтролируемое тепловыделение (экзотерма), приводящее к выбросам при масштабировании (scale-up). Добавление радикальных ингибиторов не спасает ситуацию.",
                "microscopic_candidate": "Полное разрушение защитного каркаса (disrupted confinement). Активный интермедиат становится полностью 'голым' и неселективным. Открыты все деструктивные каналы реакций (highways). Прорыв носит организационный, а не радикальный характер.",
                "validation_methods": "Спектроскопия ЯМР реакционной смеси (crude NMR — лес паразитных пиков), ГХ/ВЭЖХ (множество побочных пиков); реакторная калориметрия (ARC, RC1) для оценки термической безопасности; сравнение кинетики с радикальными ловушками и без них.",
                "example": "ДМФА + K2CO3 при 60°C, NaH в ТГФ при 25°C.",
                "framework_insight": "Защитный молекулярный каркас полностью утерян. Реагент оголён, деструктивные пути открыты. Добавление ингибиторов бесполезно — необходимо срочно менять среду (на ацетон, диоксан) или охлаждать систему до Protected-режима."
            }
