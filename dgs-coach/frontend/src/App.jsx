import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [aktifSekme, setAktifSekme] = useState("puan");

  const [konular, setKonular] = useState([]);
  const [konu, setKonu] = useState("");
  const [tahmin, setTahmin] = useState(null);
  const [gecmisVeri, setGecmisVeri] = useState([]);
  const [karsilastirmaVerisi, setKarsilastirmaVerisi] = useState([]);
  const [yukleniyor, setYukleniyor] = useState(false);
  const [hata, setHata] = useState("");

  const [soruMetni, setSoruMetni] = useState("");
  const [soruAnalizSonucu, setSoruAnalizSonucu] = useState(null);
  const [soruAnalizYukleniyor, setSoruAnalizYukleniyor] = useState(false);

  const [ogrenciPuani, setOgrenciPuani] = useState("310");
  const [arananProgram, setArananProgram] = useState("Bilgisayar Mühendisliği");
  const [tumProgramlar, setTumProgramlar] = useState([]);
  const [programOnerileri, setProgramOnerileri] = useState([]);
  const [onerilerAcik, setOnerilerAcik] = useState(false);
  const [tercihSonuclari, setTercihSonuclari] = useState([]);
  const [tercihYukleniyor, setTercihYukleniyor] = useState(false);

  const [matDogru, setMatDogru] = useState("");
  const [matYanlis, setMatYanlis] = useState("");
  const [turkceDogru, setTurkceDogru] = useState("");
  const [turkceYanlis, setTurkceYanlis] = useState("");
  const [obp, setObp] = useState("");
  const [puanTuru, setPuanTuru] = useState("SAY");
  const [puanSonucu, setPuanSonucu] = useState(null);

  useEffect(() => {
    ilkVerileriGetir();
  }, []);

  useEffect(() => {
    if (konu) {
      gecmisVeriGetir(konu);
      setTahmin(null);
    }
  }, [konu]);

  useEffect(() => {
    const arama = arananProgram.trim();

    if (arama.length < 1) {
      setProgramOnerileri([]);
      return;
    }

    const normalize = (text) =>
      String(text)
        .toLowerCase()
        .replaceAll("ı", "i")
        .replaceAll("ğ", "g")
        .replaceAll("ü", "u")
        .replaceAll("ş", "s")
        .replaceAll("ö", "o")
        .replaceAll("ç", "c");

    const anaBolumAdi = (text) =>
      String(text)
        .replace(/\s*\([^)]*\)/g, "")
        .replace(/\s+/g, " ")
        .trim();

    const aramaNormal = normalize(arama);
    const gorulen = new Set();
    const filtreli = [];

    tumProgramlar.forEach((program) => {
      const sadeAd = anaBolumAdi(program);
      const sadeNormal = normalize(sadeAd);

      if (sadeNormal.startsWith(aramaNormal) && !gorulen.has(sadeAd)) {
        gorulen.add(sadeAd);
        filtreli.push(sadeAd);
      }
    });

    setProgramOnerileri(filtreli.slice(0, 10));
    setOnerilerAcik(true);
  }, [arananProgram, tumProgramlar]);

  const ilkVerileriGetir = async () => {
    try {
      setHata("");

      const konuResponse = await fetch(`${API_URL}/konular`);
      const konuData = await konuResponse.json();

      const karsilastirmaResponse = await fetch(`${API_URL}/karsilastirma`);
      const karsilastirmaData = await karsilastirmaResponse.json();

      const programResponse = await fetch(`${API_URL}/programlar`);
      const programData = await programResponse.json();

      setKonular(konuData.konular || []);
      setKarsilastirmaVerisi(karsilastirmaData.veri || []);
      setTumProgramlar(programData.programlar || []);

      if (konuData.konular && konuData.konular.length > 0) {
        setKonu(konuData.konular[0]);
      }
    } catch (error) {
      setHata("Backend bağlantısı kurulamadı. FastAPI çalışıyor mu kontrol et.");
    }
  };

  const gecmisVeriGetir = async (secilenKonu) => {
    try {
      const response = await fetch(
        `${API_URL}/gecmis/${encodeURIComponent(secilenKonu)}`
      );

      const data = await response.json();
      setGecmisVeri(data.veri || []);
    } catch (error) {
      setHata("Geçmiş veri alınırken hata oluştu.");
    }
  };

  const tahminGetir = async () => {
    try {
      setYukleniyor(true);
      setHata("");

      const response = await fetch(
        `${API_URL}/tahmin/${encodeURIComponent(konu)}`
      );

      const data = await response.json();

      if (data.hata) {
        setHata(data.hata);
        setTahmin(null);
      } else {
        setTahmin(data);
      }
    } catch (error) {
      setHata("Tahmin alınırken hata oluştu.");
    } finally {
      setYukleniyor(false);
    }
  };

  const soruAnalizEt = async () => {
    if (!soruMetni.trim()) {
      setHata("Lütfen analiz edilecek soru metnini gir.");
      return;
    }

    try {
      setSoruAnalizYukleniyor(true);
      setHata("");
      setSoruAnalizSonucu(null);

      const response = await fetch(`${API_URL}/soru-analiz`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          soru: soruMetni,
        }),
      });

      const data = await response.json();

      if (data.hata) {
        setHata(data.hata);
      } else {
        setSoruAnalizSonucu(data);
      }
    } catch (error) {
      setHata("Soru analizi yapılırken hata oluştu.");
    } finally {
      setSoruAnalizYukleniyor(false);
    }
  };

  const tercihOnerileriniGetir = async () => {
    if (!ogrenciPuani || !arananProgram.trim()) {
      setHata("Lütfen öğrenci puanı ve program adı gir.");
      return;
    }

    try {
      setTercihYukleniyor(true);
      setHata("");
      setTercihSonuclari([]);
      setOnerilerAcik(false);

      const response = await fetch(
        `${API_URL}/tercih-oneri?puan=${encodeURIComponent(
          ogrenciPuani
        )}&program=${encodeURIComponent(arananProgram)}`
      );

      const data = await response.json();

      if (data.hata) {
        setHata(data.hata);
      } else {
        setTercihSonuclari(data.oneriler || []);
      }
    } catch (error) {
      setHata("Tercih önerileri alınırken hata oluştu.");
    } finally {
      setTercihYukleniyor(false);
    }
  };

  const puanHesapla = () => {
    const md = Number(matDogru || 0);
    const my = Number(matYanlis || 0);
    const td = Number(turkceDogru || 0);
    const ty = Number(turkceYanlis || 0);
    const dortlukNot = Number(obp || 0);

    const matNet = Math.max(0, md - my / 4);
    const turkceNet = Math.max(0, td - ty / 4);

    if (matNet < 1 || turkceNet < 1) {
      setHata(
        "DGS puanının hesaplanması için hem Matematik hem Türkçe bölümünden en az 1 net gerekir."
      );
      setPuanSonucu(null);
      return;
    }

    if (dortlukNot < 0 || dortlukNot > 4) {
      setHata("Lütfen diploma notunu 4'lük sisteme göre 0 ile 4 arasında gir.");
      setPuanSonucu(null);
      return;
    }

    setHata("");

    const yuzlukNot = dortlukNot * 25;
    const obpPuani = Math.max(40, Math.min(80, yuzlukNot * 0.8));
    const ekPuan = obpPuani * 0.6;

    const katsayilar = {
      SAY: {
        turkce: 0.587,
        matematik: 3.439,
        taban: 146,
      },
      SÖZ: {
        turkce: 2.938,
        matematik: 0.687,
        taban: 146,
      },
      EA: {
        turkce: 1.762,
        matematik: 2.063,
        taban: 146,
      },
    };

    const secili = katsayilar[puanTuru];

    let hesaplananPuan =
      secili.taban +
      turkceNet * secili.turkce +
      matNet * secili.matematik +
      ekPuan;

    hesaplananPuan = Math.max(100, Math.min(500, hesaplananPuan));

    const sonuc = {
      matNet: Number(matNet.toFixed(2)),
      turkceNet: Number(turkceNet.toFixed(2)),
      toplamNet: Number((matNet + turkceNet).toFixed(2)),
      dortlukNot: Number(dortlukNot.toFixed(2)),
      yuzlukNot: Number(yuzlukNot.toFixed(2)),
      obpPuani: Number(obpPuani.toFixed(2)),
      ekPuan: Number(ekPuan.toFixed(2)),
      puan: Number(hesaplananPuan.toFixed(2)),
    };

    setPuanSonucu(sonuc);
    setOgrenciPuani(String(sonuc.puan));
  };

  const grafikVerisi = tahmin
    ? [
        ...gecmisVeri,
        {
          yil: tahmin.tahmin_yili,
          soru: tahmin.tahmini_soru,
        },
      ]
    : gecmisVeri;

  const guncelBarVerisi = karsilastirmaVerisi.map((item) => {
    if (tahmin && item.konu === tahmin.konu) {
      return {
        ...item,
        soru: tahmin.tahmini_soru,
      };
    }

    return item;
  });

  const durumClass = (durum) => {
    if (durum === "Uygun") {
      return "bg-emerald-100 text-emerald-700";
    }

    if (durum === "Sınırda") {
      return "bg-amber-100 text-amber-700";
    }

    if (durum === "Biraz Daha Zor") {
      return "bg-orange-100 text-orange-700";
    }

    return "bg-red-100 text-red-700";
  };

  const sekmeClass = (sekme) => {
    if (aktifSekme === sekme) {
      return "bg-slate-900 text-white shadow-lg";
    }

    return "bg-white text-slate-700 hover:bg-slate-100";
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="bg-slate-950 text-white">
        <div className="max-w-7xl mx-auto px-6 py-10">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
            <div>
              <div className="inline-flex items-center gap-2 bg-blue-500/15 text-blue-200 border border-blue-400/30 px-4 py-2 rounded-full text-sm font-semibold mb-5">
                DGS Tercih ve Sınav Karar Destek Platformu
              </div>

              <h1 className="text-5xl lg:text-6xl font-black tracking-tight mb-5">
                DGS Koçu
              </h1>

              <p className="text-xl text-slate-200 max-w-4xl leading-relaxed">
                DGS Koçu; öğrencinin tahmini puanını, hedeflediği bölümü ve
                geçmiş yerleştirme verilerini birlikte değerlendirerek tercih
                sürecini daha anlaşılır, planlı ve güvenli hale getiren akıllı
                bir tercih asistanıdır.
              </p>

              <p className="text-slate-400 max-w-4xl mt-4">
                Puanını hesapla, hedef bölümünü ara, geçmiş taban puanları gör
                ve 2026 tahmini değerlere göre tercihinin sana ne kadar uygun
                olduğunu öğren.
              </p>

              <div className="flex flex-wrap gap-3 mt-7">
                <span className="bg-white/10 border border-white/10 px-4 py-2 rounded-full text-sm">
                  Tahmini Puan Hesaplama
                </span>

                <span className="bg-white/10 border border-white/10 px-4 py-2 rounded-full text-sm">
                  Tercih Uygunluk Analizi
                </span>

                <span className="bg-white/10 border border-white/10 px-4 py-2 rounded-full text-sm">
                  2026 Taban Puan Tahmini
                </span>

                <span className="bg-white/10 border border-white/10 px-4 py-2 rounded-full text-sm">
                  Sınav Strateji Desteği
                </span>
              </div>
            </div>

            <div className="bg-white/10 border border-white/10 rounded-3xl p-6 min-w-72">
              <p className="text-slate-300 text-sm mb-2">
                Başlangıç Noktası
              </p>

              <h2 className="text-2xl font-bold mb-4">
                Önce Puanını Hesapla
              </h2>

              <div className="space-y-3 text-sm text-slate-300">
                <p>• Matematik ve Türkçe netlerini hesapla</p>
                <p>• 4’lük diploma notunu gir</p>
                <p>• Tahmini DGS puanını gör</p>
                <p>• Puanını tercih analizinde otomatik kullan</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex flex-wrap gap-3 mb-8">
          <button
            onClick={() => setAktifSekme("puan")}
            className={`px-6 py-3 rounded-2xl font-semibold transition ${sekmeClass("puan")}`}
          >
            1. Puan Hesaplama
          </button>

          <button
            onClick={() => setAktifSekme("tercih")}
            className={`px-6 py-3 rounded-2xl font-semibold transition ${sekmeClass("tercih")}`}
          >
            2. Tercih Analizi
          </button>

          <button
            onClick={() => setAktifSekme("soruTahmini")}
            className={`px-6 py-3 rounded-2xl font-semibold transition ${sekmeClass("soruTahmini")}`}
          >
            3. Soru Dağılımı
          </button>

          <button
            onClick={() => setAktifSekme("nlp")}
            className={`px-6 py-3 rounded-2xl font-semibold transition ${sekmeClass("nlp")}`}
          >
            4. Soru Analizi
          </button>

          <button
            onClick={() => setAktifSekme("hakkinda")}
            className={`px-6 py-3 rounded-2xl font-semibold transition ${sekmeClass("hakkinda")}`}
          >
            Hakkında
          </button>
        </div>

        {hata && (
          <div className="bg-red-100 border border-red-300 text-red-700 rounded-2xl p-4 mb-6">
            {hata}
          </div>
        )}

        {aktifSekme === "puan" && (
          <div className="space-y-8">
            <div className="bg-white rounded-3xl p-8 shadow">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
                <div>
                  <h2 className="text-3xl font-bold mb-2">
                    DGS Tahmini Puan Hesaplama
                  </h2>

                  <p className="text-slate-600 max-w-4xl">
                    Matematik ve Türkçe doğru-yanlış sayılarını girerek netlerini
                    hesapla. 4’lük diploma notunu ekleyerek tahmini DGS puanını
                    oluştur ve bu puanı tercih analizinde otomatik kullan.
                  </p>
                </div>

                <div className="bg-blue-50 text-blue-700 px-5 py-3 rounded-2xl font-semibold">
                  Puan → Tercih Analizi
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-50 rounded-2xl p-5 border">
                  <h3 className="text-xl font-bold mb-4">Matematik</h3>

                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Doğru Sayısı
                  </label>
                  <input
                    type="number"
                    value={matDogru}
                    onChange={(e) => setMatDogru(e.target.value)}
                    className="w-full p-4 rounded-2xl border mb-4"
                    placeholder="Örnek: 35"
                  />

                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Yanlış Sayısı
                  </label>
                  <input
                    type="number"
                    value={matYanlis}
                    onChange={(e) => setMatYanlis(e.target.value)}
                    className="w-full p-4 rounded-2xl border"
                    placeholder="Örnek: 10"
                  />
                </div>

                <div className="bg-slate-50 rounded-2xl p-5 border">
                  <h3 className="text-xl font-bold mb-4">Türkçe</h3>

                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Doğru Sayısı
                  </label>
                  <input
                    type="number"
                    value={turkceDogru}
                    onChange={(e) => setTurkceDogru(e.target.value)}
                    className="w-full p-4 rounded-2xl border mb-4"
                    placeholder="Örnek: 30"
                  />

                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Yanlış Sayısı
                  </label>
                  <input
                    type="number"
                    value={turkceYanlis}
                    onChange={(e) => setTurkceYanlis(e.target.value)}
                    className="w-full p-4 rounded-2xl border"
                    placeholder="Örnek: 8"
                  />
                </div>

                <div className="bg-slate-50 rounded-2xl p-5 border">
                  <h3 className="text-xl font-bold mb-4">Puan Bilgisi</h3>

                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Diploma Notu 4'lük Sistem
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="4"
                    value={obp}
                    onChange={(e) => setObp(e.target.value)}
                    className="w-full p-4 rounded-2xl border mb-4"
                    placeholder="Örnek: 3.25"
                  />

                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Puan Türü
                  </label>
                  <select
                    value={puanTuru}
                    onChange={(e) => setPuanTuru(e.target.value)}
                    className="w-full p-4 rounded-2xl border bg-white"
                  >
                    <option value="SAY">Sayısal</option>
                    <option value="EA">Eşit Ağırlık</option>
                    <option value="SÖZ">Sözel</option>
                  </select>
                </div>
              </div>

              <div className="flex flex-col md:flex-row gap-4 mt-6">
                <button
                  onClick={puanHesapla}
                  className="bg-indigo-600 text-white px-8 py-4 rounded-2xl text-lg font-semibold hover:bg-indigo-700 transition"
                >
                  Tahmini Puanı Hesapla
                </button>

                <button
                  onClick={() => {
                    setMatDogru("");
                    setMatYanlis("");
                    setTurkceDogru("");
                    setTurkceYanlis("");
                    setObp("");
                    setPuanSonucu(null);
                  }}
                  className="bg-slate-200 text-slate-700 px-8 py-4 rounded-2xl text-lg font-semibold hover:bg-slate-300 transition"
                >
                  Temizle
                </button>
              </div>

              {puanSonucu && (
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-7 gap-4 mt-8">
                  <div className="bg-slate-100 rounded-2xl p-5">
                    <p className="text-slate-500">Matematik Net</p>
                    <h3 className="text-3xl font-bold">{puanSonucu.matNet}</h3>
                  </div>

                  <div className="bg-slate-100 rounded-2xl p-5">
                    <p className="text-slate-500">Türkçe Net</p>
                    <h3 className="text-3xl font-bold">{puanSonucu.turkceNet}</h3>
                  </div>

                  <div className="bg-slate-100 rounded-2xl p-5">
                    <p className="text-slate-500">Toplam Net</p>
                    <h3 className="text-3xl font-bold">{puanSonucu.toplamNet}</h3>
                  </div>

                  <div className="bg-slate-100 rounded-2xl p-5">
                    <p className="text-slate-500">4'lük Not</p>
                    <h3 className="text-3xl font-bold">{puanSonucu.dortlukNot}</h3>
                  </div>

                  <div className="bg-slate-100 rounded-2xl p-5">
                    <p className="text-slate-500">100'lük Not</p>
                    <h3 className="text-3xl font-bold">{puanSonucu.yuzlukNot}</h3>
                  </div>

                  <div className="bg-slate-100 rounded-2xl p-5">
                    <p className="text-slate-500">Ek Puan</p>
                    <h3 className="text-3xl font-bold">{puanSonucu.ekPuan}</h3>
                  </div>

                  <div className="bg-blue-700 text-white rounded-2xl p-5">
                    <p className="text-blue-100">Tahmini Puan</p>
                    <h3 className="text-4xl font-bold">{puanSonucu.puan}</h3>
                  </div>
                </div>
              )}

              {puanSonucu && (
                <div className="bg-blue-50 border border-blue-200 text-blue-800 rounded-2xl p-5 mt-6">
                  Hesaplanan puan tercih analizi panelindeki “Tahmini DGS Puanı”
                  alanına otomatik aktarıldı. Şimdi “Tercih Analizi” sekmesine
                  geçip hedef bölümünü arayabilirsin.
                </div>
              )}

              <p className="text-sm text-slate-500 mt-5">
                Not: Bu hesaplama yaklaşık sonuç verir. Gerçek DGS puanı, sınav
                yılındaki aday ortalamaları ve standart sapma değerleriyle ÖSYM
                tarafından hesaplanır.
              </p>
            </div>
          </div>
        )}

        {aktifSekme === "tercih" && (
          <div className="space-y-8">
            <div className="bg-white rounded-3xl p-8 shadow">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
                <div>
                  <h2 className="text-3xl font-bold mb-2">
                    Tercih ve Taban Puan Analizi
                  </h2>

                  <p className="text-slate-600 max-w-4xl">
                    Tahmini DGS puanını ve hedef bölümünü gir. Sistem, geçmiş
                    yerleştirme verilerinden oluşturulan 2026 tahmini taban
                    puanlara göre tercihin senin için uygun olup olmadığını yorumlar.
                  </p>
                </div>

                <div className="bg-blue-50 text-blue-700 px-5 py-3 rounded-2xl font-semibold">
                  Ana Modül
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Tahmini DGS Puanı
                  </label>

                  <input
                    type="number"
                    value={ogrenciPuani}
                    onChange={(e) => setOgrenciPuani(e.target.value)}
                    className="w-full p-4 rounded-2xl border text-lg bg-slate-50"
                    placeholder="Örnek: 310"
                  />
                </div>

                <div className="md:col-span-2 relative">
                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Program / Bölüm Ara
                  </label>

                  <input
                    type="text"
                    value={arananProgram}
                    onChange={(e) => {
                      setArananProgram(e.target.value);
                      setOnerilerAcik(true);
                    }}
                    onFocus={() => setOnerilerAcik(true)}
                    className="w-full p-4 rounded-2xl border text-lg bg-slate-50"
                    placeholder="Örnek: Hemşirelik, İşletme, Makine Mühendisliği"
                  />

                  {onerilerAcik && programOnerileri.length > 0 && (
                    <div className="absolute z-20 mt-2 w-full bg-white border rounded-2xl shadow-xl overflow-hidden">
                      <div className="px-5 py-2 text-xs text-slate-500 bg-slate-50 border-b">
                        Önerilen bölümler
                      </div>

                      {programOnerileri.map((item) => (
                        <button
                          key={item}
                          onClick={() => {
                            setArananProgram(item);
                            setOnerilerAcik(false);
                          }}
                          className="w-full text-left px-5 py-3 hover:bg-slate-100 border-b last:border-b-0"
                        >
                          {item}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              <div className="flex flex-col md:flex-row gap-4 mt-5">
                <button
                  onClick={tercihOnerileriniGetir}
                  disabled={tercihYukleniyor}
                  className="bg-indigo-600 text-white px-8 py-4 rounded-2xl text-lg font-semibold hover:bg-indigo-700 transition disabled:bg-slate-400"
                >
                  {tercihYukleniyor
                    ? "Tercihler Analiz Ediliyor..."
                    : "Tercih Önerilerini Getir"}
                </button>

                <button
                  onClick={() => {
                    setOgrenciPuani("");
                    setArananProgram("");
                    setTercihSonuclari([]);
                    setProgramOnerileri([]);
                  }}
                  className="bg-slate-200 text-slate-700 px-8 py-4 rounded-2xl text-lg font-semibold hover:bg-slate-300 transition"
                >
                  Temizle
                </button>
              </div>
            </div>

            {tercihSonuclari.length > 0 && (
              <div className="bg-white rounded-3xl p-8 shadow">
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
                  <div>
                    <h3 className="text-2xl font-bold">
                      Tercih Sonuçları
                    </h3>

                    <p className="text-slate-500 mt-1">
                      {ogrenciPuani} puan ile “{arananProgram}” araması için
                      uygunluk durumuna göre 50 sonuç listeleniyor.
                    </p>
                  </div>

                  <div className="bg-slate-100 rounded-2xl px-5 py-3">
                    <p className="text-slate-500 text-sm">Bulunan Sonuç</p>
                    <p className="text-2xl font-bold">{tercihSonuclari.length}</p>
                  </div>
                </div>

                <div className="overflow-x-auto rounded-2xl border">
                  <table className="w-full bg-white text-sm">
                    <thead className="bg-slate-900 text-white">
                      <tr>
                        <th className="p-3 text-left">Üniversite</th>
                        <th className="p-3 text-left">Program</th>
                        <th className="p-3 text-left">Tür</th>
                        <th className="p-3 text-left">Son Yıl Taban</th>
                        <th className="p-3 text-left">2026 Tahmini</th>
                        <th className="p-3 text-left">Kontenjan</th>
                        <th className="p-3 text-left">Fark</th>
                        <th className="p-3 text-left">Durum</th>
                      </tr>
                    </thead>

                    <tbody>
                      {tercihSonuclari.map((item, index) => (
                        <tr
                          key={`${item.program_kodu}-${index}`}
                          className="border-b hover:bg-slate-50"
                        >
                          <td className="p-3 min-w-72">
                            <p className="font-semibold text-slate-800">
                              {item.universite}
                            </p>

                            {item.fakulte && (
                              <p className="text-xs text-slate-500 mt-1">
                                {item.fakulte}
                              </p>
                            )}
                          </td>

                          <td className="p-3 min-w-56">
                            {item.program_adi}
                          </td>

                          <td className="p-3">
                            {item.puan_turu}
                          </td>

                          <td className="p-3">
                            {item.son_yil_taban_puan}
                          </td>

                          <td className="p-3 font-bold text-indigo-700">
                            {item.tahmini_taban_puan_2026}
                          </td>

                          <td className="p-3">
                            {item.tahmini_kontenjan_2026}
                          </td>

                          <td className="p-3">
                            {item.puan_farki}
                          </td>

                          <td className="p-3 min-w-44">
                            <span
                              className={`inline-block px-3 py-1 rounded-full font-semibold ${durumClass(
                                item.durum
                              )}`}
                            >
                              {item.durum}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <p className="text-sm text-slate-500 mt-4">
                  Not: Bu analiz geçmiş yerleştirme verilerine göre yapılan
                  tahmini bir uygunluk değerlendirmesidir. Resmî tercih sonucu
                  garanti etmez.
                </p>
              </div>
            )}
          </div>
        )}

        {aktifSekme === "soruTahmini" && (
          <div className="space-y-8">
            <div className="bg-white rounded-3xl p-8 shadow">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
                <div>
                  <h2 className="text-3xl font-bold mb-2">
                    DGS Matematik Soru Dağılımı Tahmini
                  </h2>

                  <p className="text-slate-600 max-w-4xl">
                    Geçmiş yıllardaki Matematik konu dağılımlarını inceleyerek
                    2026 yılında hangi konulardan kaç soru gelebileceğine dair
                    tahmini bir analiz sunar.
                  </p>
                </div>

                <div className="bg-slate-100 text-slate-700 px-5 py-3 rounded-2xl font-semibold">
                  Ek Analiz Modülü
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div>
                  <label className="block text-sm font-semibold text-slate-600 mb-2">
                    Konu Seç
                  </label>

                  <select
                    value={konu}
                    onChange={(e) => setKonu(e.target.value)}
                    className="w-full mb-4 p-4 rounded-2xl border text-lg bg-white"
                  >
                    {konular.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>

                  <button
                    onClick={tahminGetir}
                    disabled={!konu || yukleniyor}
                    className="w-full bg-blue-600 text-white py-4 rounded-2xl text-lg font-semibold hover:bg-blue-700 transition disabled:bg-slate-400"
                  >
                    {yukleniyor ? "Tahmin Yapılıyor..." : "Tahmin Getir"}
                  </button>

                  {tahmin && (
                    <div className="mt-6 bg-slate-100 rounded-2xl p-6">
                      <h3 className="text-xl font-bold mb-4">
                        Tahmin Sonucu
                      </h3>

                      <p>
                        <b>Konu:</b> {tahmin.konu}
                      </p>

                      <p>
                        <b>Model:</b> {tahmin.model}
                      </p>

                      <p>
                        <b>Tahmin Yılı:</b> {tahmin.tahmin_yili}
                      </p>

                      <div className="mt-5 bg-white rounded-2xl p-5 text-center">
                        <p className="text-slate-500 mb-1">
                          Tahmini Soru Sayısı
                        </p>

                        <p className="text-5xl font-bold text-blue-700">
                          {tahmin.tahmini_soru}
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                <div className="lg:col-span-2">
                  <h3 className="text-xl font-bold mb-2">
                    {konu || "Konu"} Yıllara Göre Soru Dağılımı
                  </h3>

                  <p className="text-slate-500 mb-6">
                    Çizgi grafikte geçmiş yıllardaki soru sayıları ve tahmin
                    yapıldığında 2026 değeri gösterilir.
                  </p>

                  <div className="h-96">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={grafikVerisi}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="yil" />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        <Line
                          type="monotone"
                          dataKey="soru"
                          strokeWidth={3}
                          dot={{ r: 5 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-3xl p-8 shadow">
              <h2 className="text-2xl font-bold mb-2">
                Konu Bazlı Karşılaştırma
              </h2>

              <p className="text-slate-500 mb-6">
                Son yıl verilerine göre konu bazlı soru dağılımlarını karşılaştırır.
              </p>

              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={guncelBarVerisi}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="konu"
                      angle={-35}
                      textAnchor="end"
                      height={120}
                      interval={0}
                    />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Bar dataKey="soru" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {aktifSekme === "nlp" && (
          <div className="bg-white rounded-3xl p-8 shadow">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
              <div>
                <h2 className="text-3xl font-bold mb-2">
                  Soru Analiz Paneli
                </h2>

                <p className="text-slate-600 max-w-4xl">
                  Çözmekte zorlandığın matematik sorusunu yaz. Sistem, soru
                  metnini inceleyerek hangi konuya yakın olduğunu tahmin eder
                  ve sana çalışma tavsiyesi verir.
                </p>
              </div>

              <div className="bg-orange-100 text-orange-700 px-5 py-3 rounded-2xl font-semibold">
                Deneysel Modül
              </div>
            </div>

            <textarea
              value={soruMetni}
              onChange={(e) => setSoruMetni(e.target.value)}
              placeholder="Örnek: 2 üzeri x eşittir 64 ise x kaçtır?"
              className="w-full min-h-40 p-5 rounded-2xl border text-lg bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <div className="flex flex-col md:flex-row gap-4 mt-4">
              <button
                onClick={soruAnalizEt}
                disabled={soruAnalizYukleniyor}
                className="bg-blue-600 text-white px-8 py-4 rounded-2xl text-lg font-semibold hover:bg-blue-700 transition disabled:bg-slate-400"
              >
                {soruAnalizYukleniyor
                  ? "Analiz Ediliyor..."
                  : "Soruyu Analiz Et"}
              </button>

              <button
                onClick={() => {
                  setSoruMetni("");
                  setSoruAnalizSonucu(null);
                }}
                className="bg-slate-200 text-slate-700 px-8 py-4 rounded-2xl text-lg font-semibold hover:bg-slate-300 transition"
              >
                Temizle
              </button>
            </div>

            {soruAnalizSonucu && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
                <div className="bg-slate-100 rounded-2xl p-6">
                  <p className="text-slate-500 mb-2">
                    Tespit Edilen Konu
                  </p>
                  <h3 className="text-3xl font-bold text-indigo-700">
                    {soruAnalizSonucu.tespit_edilen_konu}
                  </h3>
                </div>

                <div className="bg-slate-100 rounded-2xl p-6">
                  <p className="text-slate-500 mb-2">
                    Eksik Alan
                  </p>
                  <h3 className="text-xl font-bold text-slate-800">
                    {soruAnalizSonucu.eksik}
                  </h3>
                </div>

                <div className="bg-slate-100 rounded-2xl p-6">
                  <p className="text-slate-500 mb-2">
                    Çalışma Tavsiyesi
                  </p>
                  <p className="text-slate-700 leading-relaxed">
                    {soruAnalizSonucu.tavsiye}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {aktifSekme === "hakkinda" && (
          <div className="space-y-8">
            <div className="bg-white rounded-3xl p-8 shadow">
              <h2 className="text-4xl font-bold mb-4">
                DGS Koçu Nedir?
              </h2>

              <p className="text-slate-600 leading-relaxed text-lg max-w-5xl">
                DGS Koçu, Dikey Geçiş Sınavı’na hazırlanan öğrencilerin tercih
                döneminde daha bilinçli karar verebilmesi için geliştirilmiş
                akıllı bir tercih ve sınav analiz platformudur. Öğrencinin
                tahmini puanını, hedeflediği bölümü ve geçmiş yerleştirme
                verilerini birlikte değerlendirerek tercihlerin ne kadar uygun
                olduğunu anlaşılır bir şekilde gösterir.
              </p>

              <p className="text-slate-600 leading-relaxed text-lg mt-4 max-w-5xl">
                Platformun amacı, öğrencinin sadece puanına bakarak karar vermesi
                yerine; geçmiş taban puan değişimlerini, kontenjan hareketlerini
                ve bölüm bazlı eğilimleri dikkate alarak daha güvenli bir tercih
                listesi oluşturmasına yardımcı olmaktır.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="bg-white rounded-3xl p-6 shadow">
                <h3 className="text-xl font-bold mb-3">
                  Tercihlerini Daha Net Gör
                </h3>

                <p className="text-slate-600">
                  Hedeflediğin bölümü arayarak geçmiş yıllardaki taban puanları
                  ve 2026 tahmini değerlerini tek ekranda karşılaştırabilirsin.
                </p>
              </div>

              <div className="bg-white rounded-3xl p-6 shadow">
                <h3 className="text-xl font-bold mb-3">
                  Puanına Göre Yorum Al
                </h3>

                <p className="text-slate-600">
                  Sistem, tahmini puanın ile bölümün tahmini taban puanını
                  karşılaştırır ve tercihi “Uygun”, “Sınırda” veya “Zor” olarak
                  yorumlar.
                </p>
              </div>

              <div className="bg-white rounded-3xl p-6 shadow">
                <h3 className="text-xl font-bold mb-3">
                  Sınav Stratejini Güçlendir
                </h3>

                <p className="text-slate-600">
                  Ek analiz modülleri sayesinde DGS Matematik konu dağılımlarını
                  inceleyebilir ve hangi konulara daha fazla odaklanman gerektiğini
                  görebilirsin.
                </p>
              </div>
            </div>

            <div className="bg-white rounded-3xl p-8 shadow">
              <h2 className="text-2xl font-bold mb-4">
                Kimler İçin?
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-5 text-slate-600">
                <p>
                  <b>DGS’ye hazırlanan öğrenciler:</b> Puanına göre hangi
                  bölümlerin daha ulaşılabilir olduğunu görmek isteyenler.
                </p>

                <p>
                  <b>Tercih listesi hazırlayan adaylar:</b> Uygun, sınırda ve
                  riskli tercihleri daha net ayırmak isteyenler.
                </p>

                <p>
                  <b>Hedef bölüm belirleyenler:</b> Bir bölümün yıllara göre
                  nasıl değiştiğini analiz etmek isteyenler.
                </p>

                <p>
                  <b>Çalışma planı yapanlar:</b> Ek soru dağılımı analizleriyle
                  sınav hazırlığını daha stratejik yönetmek isteyenler.
                </p>
              </div>
            </div>

            <div className="bg-slate-900 text-white rounded-3xl p-8 shadow">
              <h2 className="text-2xl font-bold mb-4">
                Kısa Özet
              </h2>

              <p className="text-slate-300 leading-relaxed text-lg">
                DGS Koçu; puan hesaplama, tercih uygunluğu, taban puan tahmini
                ve sınav konu analizi özelliklerini tek platformda birleştirerek
                öğrencinin DGS sürecinde daha bilinçli ve güvenli karar vermesine
                yardımcı olur.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;